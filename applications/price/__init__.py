#coding: utf-8

from flask import Blueprint
from applications.price.resource import PriceParishByGood, PriceResource, PriceHelperResource, PriceBulkResource, \
    PriceParishByGood2

from resources import MyApi


blueprint = Blueprint('price_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.add_resource(PriceParishByGood, '/good/<int:id>/priceparish')
api.add_resource(PriceParishByGood2, '/price/togood/<int:id>')
api.add_resource(PriceResource, '/price')
api.add_resource(PriceHelperResource, '/price/getprice')
api.add_resource(PriceBulkResource, '/pricebulk')