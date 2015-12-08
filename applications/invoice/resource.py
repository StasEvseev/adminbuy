# coding: utf-8

import json
from flask import request
from flask.ext.restful import fields
import sqlalchemy
from sqlalchemy import asc
from applications.acceptance.model import Acceptance
from models.invoice import Invoice
from models.invoiceitem import InvoiceItem
from resources.core import BaseCanoniseResource, BaseInnerCanon

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


class InvoiceCanon(BaseCanoniseResource):
    model = Invoice

    attr_json = ATTR


class InvoiceItemInnerCanon(BaseInnerCanon):
    inner_model = Invoice
    model = InvoiceItem

    attr_json = ATTR_ITEMS

    def query_initial(self, inner_id, **kwargs):
        query = super(InvoiceItemInnerCanon, self).query_initial(
            inner_id, **kwargs)

        if "exclude_good_id" in request.values:
            # фильтруем товары для исключения дубляжей
            exc_good_id = request.values.get("exclude_good_id")
            exc_good_id = json.loads(exc_good_id)
            query = query.filter(
                ~InvoiceItem.good_id.in_(exc_good_id)
            )

        return query.order_by(asc(InvoiceItem.id))


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
