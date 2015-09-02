#coding: utf-8

from flask.ext.restful import marshal_with, fields
from sqlalchemy import asc
from log import error

from models.invoiceitem import InvoiceItem

from resources.core import BaseTokeniseResource


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
        from services import InvoiceService
        return {'items': InvoiceService.get_items(invoice_id)}


class InvoiceItemCountResource(BaseTokeniseResource):
    @marshal_with({'result': fields.Nested({'count': fields.Integer})})
    def get(self, invoice_id):
        from services import InvoiceService
        count = InvoiceService.get_count_items(invoice_id)
        return {'result': {'count': count}}


class InvoicePriceItemsResource(BaseTokeniseResource):
    """
    ресурс для получения товаров, цен, и их рекомендуемую стоимость на товары из накладной
    """

    @marshal_with({'items': fields.List(fields.Nested({
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
    }))})
    def get(self, mail_id):
        from services import MailInvoiceService
        from applications.price.service import PriceService

        try:

            mail = MailInvoiceService.get_mail(mail_id)
            invoice = mail.invoice

            items = PriceService.generate_price_stub(invoice.items.order_by(asc(InvoiceItem.id)))

            return {'items': [{
                'id_commodity': it.id_commodity,
                'id_good': it.id_good,
                'full_name': it.full_name,
                'number_local': it.number_local,
                'number_global': it.number_global,
                'NDS': it.NDS,
                'price_prev': it.price_prev,
                'price_post': it.price_post,
                'price_retail': it.price_retail,
                'price_gross': it.price_gross,
                'price_retail_recommendation': it.price_retail_recommendation,
                'price_gross_recommendation': it.price_gross_recommendation,
                'is_change': it.is_change
            } for it in items]}
        except Exception as exc:
            error(unicode(exc))
            raise