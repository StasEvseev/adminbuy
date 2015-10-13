#coding: utf-8

__author__ = 'StasEvseev'

from flask import Blueprint

from applications.waybill_return.resource import WayBillReturnStatusResource, WayBillReturnItemInnerCanon, \
    WayBillReturnCanon, WayBillReturnPrint
from resources import MyApi


blueprint = Blueprint('waybillreturn_blueprint', __name__)
api = MyApi(blueprint, prefix='/api')
api.register_canon(WayBillReturnCanon, "/waybillreturn")
api.register_canon(WayBillReturnItemInnerCanon, '/waybillreturn')
api.add_resource(WayBillReturnStatusResource, '/waybillreturn/<int:id>/status')
api.add_resource(WayBillReturnPrint, '/waybillreturn/print/<int:id>')