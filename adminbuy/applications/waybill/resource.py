# coding: utf-8

import json

import os
import uuid

from flask import url_for, request
from flask.ext.restful import marshal_with, fields, reqparse, abort
from sqlalchemy.orm import joinedload

from adminbuy.db import db

from adminbuy.applications.good.service import GoodService
from adminbuy.resources.core import (BaseTokeniseResource,
                                     BaseCanoniseResource, BaseInnerCanon)
from adminbuy.services.helperserv import HelperService

from .constant import GOOD_ATTR, COUNT_ATTR
from adminbuy.applications.waybill.models import WayBill, WayBillItems, FINISH
from .service import WayBillService, WayBillServiceException

from config import PATH_TO_GENERATE_INVOICE

from log import error, debug, warning


ITEM = {
        'id': fields.Integer,
        'date': fields.String,
        'number': fields.String,
        'pointsale_from_id': fields.Integer,
        'pointsale_from': fields.String(attribute="pointsale_from.name"),
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
        'invoice_id': fields.Integer,
        'invoice': fields.String,
        'filepath': fields.String,
        'rec': fields.String
    }

item = {'id': fields.Integer,
        'date': fields.String,
        'number': fields.String,
        'pointsale_from_id': fields.Integer,
        'pointsale_from': fields.String,
        'receiver_id': fields.Integer,
        'receiver': fields.String,
        'pointsale_id': fields.Integer,
        'pointsale': fields.String,
        'point': fields.String,
        'type': fields.Integer(attribute='type.code'),
        'type_str': fields.String(attribute='type.value'),
        'invoice_id': fields.Integer,
        'invoice': fields.String,
        'filepath': fields.String}

item_items = {
    'id': fields.Integer,
    'full_name': fields.String,
    'good_id': fields.Integer,
    'count_invoice': fields.Integer(default=""),
    'count': fields.Integer(default=""),
    'price': fields.String,
    'price_gross': fields.String,
    'price_retail': fields.String,
    'is_approve': fields.Boolean
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
    COUNT_ATTR: fields.Integer
}


def convert_itemitems_to_json(item, type):
    price = GoodService.get_price(item.good_id)

    return {
        'id': item.id,
        'full_name': item.good.full_name,
        'good_id': item.good_id,
        'count_invoice': item.count,
        'price': price.price_retail if type == 1 else price.price_gross,
        'price_gross': price.price_gross,
        'price_retail': price.price_retail,
        'is_approve': True
    }


def convert_item_to_json(item_waybill):
    return {
        'id': item_waybill.id,
        'date': item_waybill.date,
        'number': item_waybill.number,
        'pointsale_from_id': item_waybill.pointsale_from_id,
        'pointsale_from': item_waybill.pointsale_from.name
        if item_waybill.pointsale_from else None,
        'receiver_id': item_waybill.receiver_id or None,
        'receiver': item_waybill.receiver.fullname
        if item_waybill.receiver else None,
        'pointsale_id': item_waybill.pointsale_id or None,
        'pointsale': item_waybill.pointsale.name
        if item_waybill.pointsale else None,
        'point': item_waybill.rec,
        'type': item_waybill.type,
        'type_str': item_waybill.typeS,
        'invoice_id': item_waybill.invoice_id or None,
        'invoice': item_waybill.invoice,
        'filepath': item_waybill.filepath
    }


parser = reqparse.RequestParser()
parser.add_argument('invoice_id', type=int)
parser.add_argument('receiver_id', type=int)
parser.add_argument('pointsale_id', type=int)
parser.add_argument('type', type=int)


class WayBillHelperResource(BaseTokeniseResource):
    @marshal_with({'data': fields.Nested(item),
                   'status': fields.Boolean,
                   'extra': fields.String})
    def get(self):
        args = parser.parse_args()
        invoice_id = args['invoice_id']
        receiver_id = args['receiver_id']
        pointsale_id = args['pointsale_id']
        type = args['type']

        count = WayBillService.count_exists(invoice_id, receiver_id,
                                            pointsale_id, type)
        if count:
            if count > 1:
                return {'status': True, 'extra': 'multi'}
            else:
                waybill = WayBillService.get_by_attr(invoice_id, receiver_id,
                                                     pointsale_id, type)
                return {'status': True, 'data': waybill, 'extra': 'single'}
        else:
            return {'status': False}


class WayBillBulk(BaseTokeniseResource):
    def post(self):
        try:
            debug(u"Сохранение пачки накладных.")
            pointSource = request.json['pointSource']
            pointitems = request.json['pointReceiver']
            items = request.json['items']
            date = request.json['date']
            date = HelperService.convert_to_pydate(date)
            type = request.json['type']
            typeRec = request.json['typeRec']
            for it in items:
                it['count'] = 0
            for item in pointitems:
                waybill = WayBillService.create(
                    pointSource['id'], None, date, None, item['id'], type,
                    typeRec)
                waybill.waybill_items = items
                if waybill.waybill_items:
                    debug(u"Сохранение позиций накладной %s." % waybill)
                    try:
                        waybill_items = WayBillService.build_retail_items(
                            waybill.waybill_items)
                    except Exception as exc:
                        debug(u"Ошибка сохранения накладной %s. " + unicode(
                            exc) % waybill)
                        raise WayBillCanon.WayBillCanonException(unicode(exc))

                    WayBillService.upgrade_items(waybill, waybill_items)
        except Exception as exc:
            db.session.rollback()
            debug(u"Сохранение накладной %s не удалось." % unicode(exc))
            abort(400, message=unicode(exc))

        db.session.commit()
        return "ok"


class WayBillItemInnerCanon(BaseInnerCanon):
    inner_model = WayBill
    model = WayBillItems

    attr_json = ITEM_ITEMS

    default_sort = "asc", "id"

    def query_initial(self, inner_id, **kwargs):
        try:
            queryset = self.model.query.options(
                joinedload('good').joinedload('price'))
            return queryset.filter_by(waybill_id=inner_id)
        except Exception as exc:
            error(u"Ошибка в инициализации запроса. " + unicode(exc))
            raise exc


class WayBillPrint(BaseTokeniseResource):
    prefix_url_with_id = "/<int:id>"

    @marshal_with({
        'link': fields.String
    })
    def get(self, id):

        path = WayBillService.report(id)

        return {"link": path}


parser = reqparse.RequestParser()
parser.add_argument('ids')


class WayBillPrintBulk(BaseTokeniseResource):
    def get(self):

        args = parser.parse_args()
        ids = json.loads(args['ids'])
        path = WayBillService.report_multi(ids)

        return {'link': path}


class WayBillCanon(BaseCanoniseResource):
    model = WayBill

    attr_json = ITEM

    multif = {"filter_field": ('number', )}

    class WayBillCanonException(BaseCanoniseResource.CanonException):
        pass

    def pre_save(self, obj, data):
        try:
            obj.date = HelperService.convert_to_pydate(data['date'])
        except KeyError as exc:
            error(u"Попытка сохранить накладную без даты. " + unicode(exc))
            raise WayBillCanon.WayBillCanonException(
                u"Для сохранения необходим обязательный параметр %s." % 'date')
        try:
            obj.waybill_items = data['items']
        except KeyError as exc:
            debug(u"Сохранение накладной %s без позиций товара." % obj)
            obj.waybill_items = []

        return super(WayBillCanon, self).pre_save(obj, data)

    def post(self, id):
        obj = super(WayBillCanon, self).post(id)
        return obj

    def save_model(self, obj):
        file_name = str(uuid.uuid4()) + ".xls"
        path_to_target = os.path.join(PATH_TO_GENERATE_INVOICE, file_name)
        try:
            if not obj.id:
                waybill = WayBillService.create(
                    obj.pointsale_from_id, obj.invoice_id, obj.date,
                    obj.receiver_id, obj.pointsale_id, obj.type,
                    obj.typeRec, forse=True)
            else:
                super(WayBillCanon, self).save_model(obj)
                waybill = obj
            if obj.waybill_items:
                debug(u"Сохранение позиций накладной %s." % obj)
                try:
                    items = WayBillService.build_retail_items(
                        obj.waybill_items)
                except Exception as exc:
                    debug(u"Ошибка сохранения накладной %s. " + unicode(
                        exc) % obj)
                    raise WayBillCanon.WayBillCanonException(unicode(exc))

                path = url_for('static', filename='files/' + file_name)
                WayBillService.upgrade_items(
                    waybill, items, path_to_target, path)
                waybill.file_load = path
            else:
                waybill.file_load = waybill.file
        except WayBillServiceException as exc:
            debug(u"Сохранение накладной %s не удалось." % obj)
            raise WayBillCanon.WayBillCanonException(unicode(exc))
        return waybill

    def put(self):
        obj = super(WayBillCanon, self).put()
        return obj

    def pre_delete(self, obj):
        if obj.status == FINISH:
            warning(u"Попытка удалить 'накладную' с финальным статусом.")
            raise BaseCanoniseResource.CanonException(
                u"Нельзя удалить 'накладную' со статусом `Завершено`.")
        else:
            obj.items.delete()
            super(WayBillCanon, self).pre_delete(obj)

    def query_initial(self, ids=None, *args, **kwargs):
        queryset = super(WayBillCanon, self).query_initial(ids, *args, **kwargs)

        queryset = queryset.options(joinedload('pointsale'))

        return queryset


class WayBillStatusResource(BaseTokeniseResource):
    @marshal_with(ITEM)
    def post(self, id):
        try:
            inventory = WayBillService.get_by_id(id)
            status = request.json['data']['status']
            WayBillService.status(inventory, status)
            db.session.add(inventory)
            db.session.commit()
            return inventory
        except Exception as exc:
            message = u" Не удалось сменить статус `накладной` %s." % id
            error(message + unicode(exc))
            abort(400, message=message)


class WayBillItemItemsResource(BaseTokeniseResource):
    @marshal_with({'items': fields.List(fields.Nested(item_items))})
    def get(self, id):
        waybill = WayBillService.get_by_id(id)
        return {'items': [convert_itemitems_to_json(x, waybill.type) for x in
                          waybill.items]}
