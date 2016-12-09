# coding: utf-8

from sqlalchemy import asc

from adminbuy.models.invoiceitem import InvoiceItem

__author__ = 'StasEvseev'


def _stub(invoice):
    from adminbuy.applications.price.service import PriceService

    items = PriceService.generate_price_stub(
        invoice.items.order_by(asc(InvoiceItem.id)))

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
