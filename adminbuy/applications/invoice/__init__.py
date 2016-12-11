# coding: utf-8

from flask import Blueprint

from adminbuy.resources import MyApi

from .resource import (InvoiceCanon, InvoiceItemInnerCanon,
                       InvoiceItemAcceptanceInnerCanon, InvoiceItemResource,
                       InvoiceItemCountResource, InvoicePrice2ItemsResource)


__author__ = 'StasEvseev'


blueprint = Blueprint('invoice_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_canon(InvoiceCanon, '/invoice_canon')
api.register_canon(InvoiceItemInnerCanon, '/invoice_canon')
api.register_canon(InvoiceItemAcceptanceInnerCanon, '/from_acceptance')

api.add_resource(InvoiceItemResource, '/invoice/<int:invoice_id>/items')
api.add_resource(InvoiceItemCountResource, '/invoice/<int:invoice_id>/count')
api.add_resource(InvoicePrice2ItemsResource, '/invoiceprice2items/<int:id>')
