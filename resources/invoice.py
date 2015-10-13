#coding: utf-8

from flask.ext.restful import marshal_with, fields
from sqlalchemy import asc
from applications.invoice.helpers import _stub
from log import error

from models.invoiceitem import InvoiceItem

from resources.core import BaseTokeniseResource


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
        'price_retail': fields.Integer(attribute='good.price.price_retail', default=''),
        'price_gross': fields.Integer(attribute='good.price.price_gross', default=''),
        'fact_count': fields.Integer(default='')
    }))})
    def get(self, invoice_id):
        from services.mailinvoice import InvoiceService
        return {'items': InvoiceService.get_items(invoice_id)}


class InvoiceItemCountResource(BaseTokeniseResource):
    @marshal_with({'result': fields.Nested({'count': fields.Integer})})
    def get(self, invoice_id):
        from services.mailinvoice import InvoiceService
        count = InvoiceService.get_count_items(invoice_id)
        return {'result': {'count': count}}


class InvoicePrice2ItemsResource(BaseTokeniseResource):
    @marshal_with(ATTR_STUB)
    def get(self, id):
        from services.mailinvoice import InvoiceService
        try:
            invoice = InvoiceService.get_by_id(id)
            return _stub(invoice)
        except Exception as exc:
            error(unicode(exc))
            raise


class InvoicePriceItemsResource(BaseTokeniseResource):
    """
    ресурс для получения товаров, цен, и их рекомендуемую стоимость на товары из накладной
    """

    @marshal_with(ATTR_STUB)
    def get(self, mail_id):
        from services.mailinvoice import MailInvoiceService

        try:

            mail = MailInvoiceService.get_mail(mail_id)
            invoice = mail.invoice

            return _stub(invoice)

        except Exception as exc:
            error(unicode(exc))
            raise