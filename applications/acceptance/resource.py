# coding: utf-8

from flask.ext.restful import marshal_with, fields

from resources import Date
from resources.core import (BaseTokeniseResource, BaseCanoniseResource,
                            BaseInnerCanon, BaseStatusResource)
from log import warning, debug

from services import HelperService, InvoiceService, ModelService

from applications.acceptance.model import (Acceptance, AcceptanceItems, MAIL,
                                           NEW, IN_PROG, VALIDATED)
from applications.acceptance.service import AcceptanceService

from db import db


ITEM = {
    'id': fields.Integer,
    'date': Date,
    'type': fields.Integer(attribute='type.code'),
    'type_str': fields.String(attribute='type.value'),
    'status': fields.Integer(attribute='status.code'),
    'status_str': fields.String(attribute='status.value'),
    'invoice_id': fields.Integer,
    'invoice_str': fields.String(attribute='invoice'),
    'receiver': fields.String,
    'provider_id': fields.Integer,
    'pointsale_id': fields.Integer,
    'pointsale_name': fields.String(attribute='pointsale.name'),
    'invoice': fields.Nested({
        'number': fields.String,
        'provider': fields.Nested({
            'id': fields.Integer,
            'name': fields.String
        })
    }, allow_null=True),
    'pointsale': fields.Nested({
        'name': fields.String
    })
}


class AcceptanceItemInnerCanon(BaseInnerCanon):
    inner_model = Acceptance
    model = AcceptanceItems

    attr_json = {
        'id': fields.Integer,
        'good': fields.Nested({
            'full_name': fields.String
        }),
        'count': fields.Integer,
        'fact_count': fields.String
    }

    default_sort = 'asc', 'id'


class AcceptanceCanon(BaseCanoniseResource):
    model = Acceptance

    attr_json = ITEM

    def pre_save(self, obj, data):
        obj = super(AcceptanceCanon, self).pre_save(obj, data)
        # TODO: отрефакторить!!!
        if obj.id is None:
            if self.model.query.filter(
                    self.model.invoice_id == obj.invoice_id).count() > 0:
                warning(u"Попытка создания приемки по расходной накладной, на "
                        u"которую уже есть приемка.")
                raise BaseCanoniseResource.CanonException(
                    u"Для расходной накладной можно создавать только одну "
                    u"приемку.")
            if 'date' not in data:
                raise BaseCanoniseResource.CanonException(
                    u"Поле дата - обязательно для заполнения.")
            obj.date = HelperService.convert_to_pydate(data['date'])
            if ('pointsale_id' not in data or
                    not ModelService.check_id(data['pointsale_id'])):
                raise BaseCanoniseResource.CanonException(
                    u"Поле торговая точка - обязательно для заполнения.")
            if 'type' not in data:
                raise BaseCanoniseResource.CanonException(
                    u"Нельзя создать приход без типа.")
            type = int(data['type'])
            if type not in [MAIL, NEW]:
                raise BaseCanoniseResource.CanonException(
                    u"Передан неверный тип.")
            if type == MAIL and not ModelService.check_id(data['invoice_id']):
                raise BaseCanoniseResource.CanonException(
                    u"При выбранном типе 'Регулярная накладная' необходимо "
                    u"указать накладную")
            if type == NEW and not ModelService.check_id(data['provider_id']):
                raise BaseCanoniseResource.CanonException(
                    u"При выбранном типе 'Новая' необходимо указать "
                    u"поставщика")
            if type == MAIL:
                obj.provider_id = None
            elif type == NEW:
                obj.invoice_id = None

        elif 'date' in data:
            obj.date = HelperService.convert_to_pydate(data['date'])
        if obj.id:
            if self.model.query.filter(
                    self.model.invoice_id == obj.invoice_id,
                    self.model.id != obj.id).count() > 0:
                raise BaseCanoniseResource.CanonException(
                    u"Для расходной накладной можно создавать только одну "
                    u"приемку.")
        return obj

    def pre_delete(self, obj):
        if obj.status == VALIDATED:
            warning(u"Попытка удалить приемку в завершенном статусе "
                    u"(%s)." % obj.id)
            raise BaseCanoniseResource.CanonException(
                u"Нельзя удалять приемку, в завершенном статусе."
            )
        if obj.type == NEW:
            debug(u"Удаление приемки с типом новой (%s). Удаляется также "
                  u"накладная." % obj.id)
            obj.invoice.items.delete()
            db.session.delete(obj.invoice)

    def post_save(self, obj, data, create_new=False):
        super(AcceptanceCanon, self).post_save(obj, data, create_new)

        if create_new is False:
            if obj.type == MAIL:
                items = data['items'] if 'items' in data else []
                AcceptanceService.update_fact_count(obj, items)
            elif obj.type == NEW and obj.status == IN_PROG:
                items = data['new_items'] if 'new_items' in data else []
                AcceptanceService.update_fact_count_custom(obj, items)


class AcceptanceStatusResource(BaseStatusResource):

    service = AcceptanceService

    @marshal_with(ITEM)
    def post(self, id):
        return self._action(id)


class AcceptanceRemainItemsResource(BaseTokeniseResource):
    @marshal_with({'items': fields.List(fields.Nested({
        'id': fields.Integer,
        'full_name': fields.String,
        'good_id': fields.Integer,
        'price_retail': fields.String,
        'price_gross': fields.String,
        'count': fields.String
    }))})
    def get(self, id):
        return {'items': InvoiceService.get_items_acceptance(id)}


class AcceptanceItemsResource(BaseTokeniseResource):
    @marshal_with({'items': fields.List(fields.Nested({
        'id': fields.Integer,
        'full_name': fields.String,
        'good_id': fields.Integer,
        "price_without_NDS": fields.String,
        "price_with_NDS": fields.String,
        'price_retail': fields.String,
        'price_gross': fields.String,
        'count': fields.String,
        'fact_count': fields.String
    }))})
    def get(self, id):

        return {'items': InvoiceService.get_items_acceptance(id, remain=False)}
