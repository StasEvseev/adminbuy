# coding: utf-8

import os
import uuid

from flask import request
from flask.ext.restful import marshal_with, fields, abort
from applications.waybill.constant import GOOD_ATTR, COUNT_ATTR
from applications.waybill_return.model import (WayBillReturn,
                                               WayBillReturnItems, RETAIL,
                                               FINISH)
from applications.waybill_return.service import WayBillReturnService
from config import PATH_TO_GENERATE_INVOICE, PATH_WEB
from db import db
from excel.output import PrintInvoice, PATH_TEMPLATE

from log import error, debug, warning

from resources.core import (BaseTokeniseResource, BaseCanoniseResource,
                            BaseInnerCanon)

from services import HelperService


ITEM = {
        'id': fields.Integer,
        'date': fields.String,
        'date_to': fields.String,
        'number': fields.String,
        'receiver_id': fields.Integer,
        'receiver': fields.String(attribute="receiver.fullname"),
        'pointsale_id': fields.Integer,
        'pointsale': fields.String(attribute="pointsale.name"),
        'point': fields.String,
        'typeRec': fields.Integer(attribute='typeRec.code'),
        'typeRec_str': fields.String(attribute='typeRec.value'),
        'type': fields.Integer(attribute='type.code'),
        'type_str': fields.String(attribute='type.value'),
        'status': fields.Integer(attribute='status.code'),
        'status_str': fields.String(attribute='status.value'),
        'returninst_id': fields.Integer,
        'returninst': fields.Nested({
            'name': fields.String
        }),
        'filepath': fields.String,
        'rec': fields.String
    }

ITEM_ITEMS = {
    'id': fields.Integer,
    'good': fields.Nested({
        'id': fields.Integer,
        'full_name': fields.String,
        'price': fields.Nested({
            'price_retail': fields.Float,
            'price_gross': fields.Float})}),
    GOOD_ATTR: fields.Integer,
    COUNT_ATTR: fields.Integer(default=''),
    'count_plan': fields.Integer
}


class WayBillReturnItemInnerCanon(BaseInnerCanon):
    inner_model = WayBillReturn
    model = WayBillReturnItems

    attr_json = ITEM_ITEMS

    default_sort = "asc", "id"


class WayBillReturnCanon(BaseCanoniseResource):
    model = WayBillReturn

    attr_json = ITEM

    class WayBillCanonException(BaseCanoniseResource.CanonException):
        pass

    def pre_save(self, obj, data):
        try:
            obj.date = HelperService.convert_to_pydate(data['date'])
            obj.date_to = HelperService.convert_to_pydate(data['date_to'])
        except KeyError as exc:
            error(u"Попытка сохранить накладную без даты. " + unicode(exc))
            raise WayBillReturnCanon.WayBillCanonException(
                u"Для сохранения необходим обязательный параметр %s." % 'date')
        try:
            obj.waybill_items = data['items']
        except KeyError as exc:
            debug(u"Сохранение накладной %s без позиций товара." % obj)
            obj.waybill_items = []
        return super(WayBillReturnCanon, self).pre_save(obj, data)

    def post(self, id):
        obj = super(WayBillReturnCanon, self).post(id)
        return obj

    def save_model(self, obj):
        try:
            if not obj.id:
                waybill = WayBillReturnService.create(
                    obj.pointsale_id, obj.receiver_id, obj.date, obj.date_to,
                    obj.type, obj.typeRec, obj.returninst_id)
            else:
                super(WayBillReturnCanon, self).save_model(obj)
                waybill = obj
            if obj.waybill_items:
                try:
                    items = WayBillReturnService.build_retail_items(
                        obj.waybill_items)
                except Exception as exc:
                    debug(u"Ошибка сохранения накладной "
                          u"%s. " + unicode(exc) % obj)
                    raise WayBillReturnCanon.WayBillCanonException(
                        unicode(exc))

                WayBillReturnService.upgrade_items(waybill, items)
        except WayBillReturnService.WayBillReturnServiceExc as exc:
            debug(u"Сохранение накладной %s не удалось." % obj)
            raise WayBillReturnCanon.WayBillCanonException(unicode(exc))

        return waybill

    def put(self):
        obj = super(WayBillReturnCanon, self).put()
        return obj

    def pre_delete(self, obj):
        if obj.status == FINISH:
            warning(u"Попытка удалить возвратную накладную в завершенном "
                    u"статусе (%s)." % obj.id)
            raise BaseCanoniseResource.CanonException(
                u"Нельзя удалять возвратную накладную, в завершенном статусе.")


class WayBillReturnStatusResource(BaseTokeniseResource):
    @marshal_with(ITEM)
    def post(self, id):
        try:
            inventory = WayBillReturnService.get_by_id(id)
            status = request.json['data']['status']
            WayBillReturnService.status(inventory, status)
            db.session.add(inventory)
            db.session.commit()

            return inventory
        except Exception as exc:
            message = (u" Не удалось сменить статус `накладной "
                       u"возврата` %s." % id)
            error(message + unicode(exc))
            abort(400, message=message)


class WayBillReturnPrint(BaseTokeniseResource):
    prefix_url_with_id = "/<int:id>"

    @marshal_with({
        'link': fields.String
    })
    def get(self, id):

        waybill = WayBillReturnService.get_by_id(id)

        file_name = str(uuid.uuid4()) + ".xls"
        path_to_target = os.path.join(PATH_TO_GENERATE_INVOICE, file_name)
        path = os.path.join(PATH_WEB, file_name)

        pi = PrintInvoice(
            path=os.path.join(PATH_TEMPLATE, 'print_waybillreturn.xls'),
            destination=path_to_target)
        pi.set_cells(0, 0, [('number', 2)])
        pi.set_cells(0, 3, ['a', 'date', 'c', 'c', 'c', 'receiver'])
        pi.set_cells(0, 4, ['a', 'date_to'])
        pi.set_cells(0, 5, ['a', 'type'])
        pi.set_cells(0, 7, [('name', 5), 'count_plan', 'count'])

        pi.write(0, 0, 0, [{'number': waybill.number}])
        pi.write(0, 3, 2, [{'date': waybill.date.strftime(
            '%d.%m.%Y').decode("utf-8"), 'receiver': waybill.rec}])
        pi.write(0, 4, 0, [{'date_to': waybill.date_to.strftime(
            '%d.%m.%Y').decode("utf-8")}])
        pi.write(0, 5, 0, [{'type': waybill.type}])

        if waybill.type == RETAIL:
            items = [
                {'name': it.good.full_name, 'count_plan': it.count_plan or "",
                 'count': it.count or ""} for it in waybill.items]
            pi.write(0, 7, 2, items)
        else:
            items = [
                {'name': it.good.full_name, 'count_plan': it.count_plan or "",
                 'count': it.count or ""} for it in waybill.items]
            pi.write(0, 7, 2, items)

        return {"link": path}
