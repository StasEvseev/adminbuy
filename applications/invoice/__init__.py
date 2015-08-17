#coding: utf-8
from flask import Blueprint

from resources import MyApi

from applications.invoice.resource import InvoiceCanon, InvoiceItemInnerCanon, InvoiceItemAcceptanceInnerCanon


blueprint = Blueprint('invoice_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_canon(InvoiceCanon, '/invoice_canon')
api.register_canon(InvoiceItemInnerCanon, '/invoice_canon')
api.register_canon(InvoiceItemAcceptanceInnerCanon, '/from_acceptance')