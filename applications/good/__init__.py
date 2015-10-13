#coding: utf-8

__author__ = 'StasEvseev'

from flask import Blueprint


from resources import MyApi
from applications.good.resource import GoodResourceCanon, GoodPrintBarcode


blueprint = Blueprint('good_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_canon(GoodResourceCanon, "/good")
api.add_resource(GoodPrintBarcode, "/good/<int:id>/printbarcode")