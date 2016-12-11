# coding: utf-8

import json

from flask import request
from flask.ext.restful import marshal_with, fields
import sqlalchemy
from sqlalchemy import asc
from sqlalchemy.orm import joinedload

from adminbuy.resources.core import (BaseCanoniseResource, BaseInnerCanon,
                                     BaseTokeniseResource)
from adminbuy.applications.invoice.helpers import _stub
from adminbuy.applications.acceptance.model import Acceptance

from .models import Invoice, InvoiceItem

from log import error


__author__ = 'StasEvseev'


ATTR = {
    'id': fields.Integer,
    'number': fields.String,
    'date': fields.String,
    'provider_id': fields.Integer,
    'provider_name': fields.String(attribute='provider.name'),
    'is_acceptance': fields.Boolean,
    'acceptance_id': fields.Integer,
    'fullname': fields.String(attribute="fullname")
}

ATTR_ITEMS = {
    'id': fields.Integer,
    'full_name': fields.String,
    'name': fields.String,
    'number_local': fields.String,
    'number_global': fields.String,
    'count_order': fields.Integer,
    'count_postorder': fields.Integer,
    'count': fields.Integer,
    'price_without_NDS': fields.String,
    'price_with_NDS': fields.String,
    'sum_without_NDS': fields.String,
    'sum_NDS': fields.String,
    'rate_NDS': fields.String,
    'sum_with_NDS': fields.String,
    'thematic': fields.String,
    'count_whole_pack': fields.Integer,
    'placer': fields.Integer,
    'fact_count': fields.Integer(default=''),

    'good_id': fields.Integer,

    'good': fields.Nested({
        'id': fields.Integer,
        'full_name': fields.String,
        'price': fields.Nested({
            'price_retail': fields.Float,
            'price_gross': fields.Float})
    }),
}

ATTR_STUB = {'items': fields.List(fields.Nested({
    'id_commodity': fields.Integer,
    'full_name': fields.String,
    'number_local': fields.String,
    'number_global': fields.String,
    'NDS': fields.String,
    'price_prev': fields.String,
    'price_post': fields.String,
    'price_retail': fields.String,
    'price_gross': fields.String,
    'price_retail_recommendation': fields.String,
    'price_gross_recommendation': fields.String,
    'is_change': fields.Boolean,
    'id_good': fields.Integer
}))}


class InvoiceCanon(BaseCanoniseResource):
    model = Invoice

    attr_json = ATTR


class InvoiceItemInnerCanon(BaseInnerCanon):
    inner_model = Invoice
    model = InvoiceItem

    attr_json = ATTR_ITEMS

    def query_initial(self, inner_id, **kwargs):
        try:
            queryset = self.model.query.options(
                joinedload('good').joinedload('price'))
            queryset = queryset.filter_by(invoice_id=inner_id)

            if "exclude_good_id" in request.values:
                # фильтруем товары для исключения дубляжей
                exc_good_id = request.values.get("exclude_good_id")
                exc_good_id = json.loads(exc_good_id)
                queryset = queryset.filter(
                    ~InvoiceItem.good_id.in_(exc_good_id)
                )
            return queryset.order_by(asc(InvoiceItem.id))
        except Exception as exc:
            error(u"Ошибка в инициализации запроса. " + unicode(exc))
            raise exc


class InvoiceItemAcceptanceInnerCanon(BaseInnerCanon):
    inner_model = Acceptance
    model = InvoiceItem

    attr_json = {
        'good': fields.Nested({
            'id': fields.Integer,
            'full_name': fields.String
        }),
        'fact_count': fields.Integer(default=''),
        'price_with_NDS': fields.String,
        'price_retail': fields.String,
        'price_gross': fields.String,
    }

    def query_initial(self, inner_id, **kwargs):

        acceptance = self.inner_model.query.get(inner_id)
        invoice = acceptance.invoice

        if invoice is None:
            query = self.model.query.filter(sqlalchemy.sql.false())
        else:
            query = invoice.items

        return query


class InvoiceItemResource(BaseTokeniseResource):
    @marshal_with({'items': fields.List(fields.Nested({
        'id': fields.Integer,
        'full_name': fields.String,
        'name': fields.String,
        'number_local': fields.String,
        'number_global': fields.String,
        'count_order': fields.Integer,
        'count_postorder': fields.Integer,
        'count': fields.Integer,
        'price_without_NDS': fields.String,
        'price_with_NDS': fields.String,
        'sum_without_NDS': fields.String,
        'sum_NDS': fields.String,
        'rate_NDS': fields.String,
        'sum_with_NDS': fields.String,
        'thematic': fields.String,
        'count_whole_pack': fields.Integer,
        'placer': fields.Integer,
        'good_id': fields.Integer,
        'commodity_id': fields.Integer(attribute='good.commodity_id'),
        'price_id': fields.Integer(attribute='good.price_id'),
        'price_retail': fields.Integer(
            attribute='good.price.price_retail', default=''),
        'price_gross': fields.Integer(
            attribute='good.price.price_gross', default=''),
        'fact_count': fields.Integer(default='')
    }))})
    def get(self, invoice_id):
        from adminbuy.services.mailinvoice import InvoiceService
        return {'items': InvoiceService.get_items(invoice_id)}


class InvoiceItemCountResource(BaseTokeniseResource):
    @marshal_with({'result': fields.Nested({'count': fields.Integer})})
    def get(self, invoice_id):
        from adminbuy.services.mailinvoice import InvoiceService
        count = InvoiceService.get_count_items(invoice_id)
        return {'result': {'count': count}}


class InvoicePrice2ItemsResource(BaseTokeniseResource):
    @marshal_with(ATTR_STUB)
    def get(self, id):
        from adminbuy.services.mailinvoice import InvoiceService
        try:
            invoice = InvoiceService.get_by_id(id)
            return _stub(invoice)
        except Exception as exc:
            error(unicode(exc))
            raise


class InvoicePriceItemsResource(BaseTokeniseResource):
    """
    ресурс для получения товаров, цен, и их рекомендуемую стоимость на товары
    из накладной
    """

    @marshal_with(ATTR_STUB)
    def get(self, mail_id):
        from adminbuy.services.mailinvoice import MailInvoiceService

        try:

            mail = MailInvoiceService.get_mail(mail_id)
            invoice = mail.invoice

            return _stub(invoice)

        except Exception as exc:
            error(unicode(exc))
            raise
