# coding: utf-8

from flask.ext.restful import marshal_with, fields
from sqlalchemy.orm import joinedload

from adminbuy.db import db
from adminbuy.resources import Date, core

from log import warning, debug, error
from ..acceptance.model import (Acceptance, AcceptanceItems, MAIL, NEW,
                                IN_PROG, VALIDATED)
from ..acceptance.service import AcceptanceService, AcceptanceException

from adminbuy.services.mailinvoice import InvoiceService


ITEM = {
    'id': fields.Integer,
    'date': Date,
    'type': fields.Integer(attribute='type.code'),
    'type_str': fields.String(attribute='type.value'),
    'status': fields.Integer(attribute='status.code'),
    'status_str': fields.String(attribute='status.value'),
    'receiver': fields.String,
    'provider_id': fields.Integer,
    'pointsale_id': fields.Integer,
    'pointsale_name': fields.String(attribute='pointsale.name'),
    'invoices': fields.Nested({
        'id': fields.Integer,
        'number': fields.String,
        'fullname': fields.String
    }),
    'pointsale': fields.Nested({
        'name': fields.String
    }),
    'display': fields.String,
    'display_invoices': fields.String
}


class AcceptanceItemInnerCanon(core.BaseInnerCanon):
    inner_model = Acceptance
    model = AcceptanceItems

    attr_json = {
        'id': fields.Integer,
        'good': fields.Nested({
            'full_name': fields.String,
            'id': fields.Integer
        }),
        'count': fields.Integer,
        'fact_count': fields.String,
        'fact_count_default': fields.String(attribute='fact_count_front')
    }

    default_sort = 'asc', 'id'

    def query_initial(self, inner_id, **kwargs):
        try:
            queryset = self.model.query.options(
                joinedload(AcceptanceItems.good))
            return queryset.filter_by(acceptance_id=inner_id)
        except Exception as exc:
            error(u"Ошибка в инициализации запроса. " + unicode(exc))
            raise exc


class AcceptanceCanon(core.BaseCanoniseResource):
    model = Acceptance

    attr_json = ITEM

    def pre_save(self, acceptance, data):
        acceptance = super(AcceptanceCanon, self).pre_save(acceptance, data)
        try:
            acceptance = AcceptanceService.prepared_acceptance(
                acceptance=acceptance,
                date=data.get('date', None),
                pointsale_id=data.get('pointsale_id', None),
                type=data.get('type', None),
                provider_id=data.get('provider_id', None),
                invoices=map(lambda x: x['id'], data.get('invoices', [])))
        except AcceptanceException as exc:
            raise core.BaseCanoniseResource.CanonException(unicode(exc))

        return acceptance

    def pre_delete(self, obj):
        if obj.status == VALIDATED:
            warning(u"Попытка удалить приемку в завершенном статусе (%s)."
                    % obj.id)
            raise core.BaseCanoniseResource.CanonException(
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


class AcceptanceStatusResource(core.BaseStatusResource):

    service = AcceptanceService

    @marshal_with(ITEM)
    def post(self, id):
        return self._action(id)


class AcceptanceRemainItemsResource(core.BaseTokeniseResource):
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


class AcceptanceItemsResource(core.BaseTokeniseResource):
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
