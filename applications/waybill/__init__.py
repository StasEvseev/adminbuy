# coding: utf-8

from flask import Blueprint
from applications.waybill.resource import (WayBillCanon, WayBillHelperResource,
                                           WayBillItemItemsResource,
                                           WayBillStatusResource,
                                           WayBillItemInnerCanon, WayBillPrint,
                                           WayBillBulk)
from resources import MyApi


blueprint = Blueprint(
    'waybill_blueprint', __name__, static_folder='static',
    template_folder='templates', static_url_path='/static/waybill')
api = MyApi(blueprint, prefix='/api')
api.add_resource(WayBillBulk, '/waybillbulk')
api.register_canon(WayBillCanon, "/waybill")
api.register_canon(WayBillItemInnerCanon, '/waybill')
api.add_resource(WayBillHelperResource, '/waybill/check_exists')
api.add_resource(WayBillStatusResource, '/waybill/<int:id>/status')
api.add_resource(WayBillPrint, '/waybill/print/<int:id>')
