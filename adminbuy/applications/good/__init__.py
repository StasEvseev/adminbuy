# coding: utf-8

from flask import Blueprint

from adminbuy.resources import MyApi

from .resource import GoodResourceCanon, GoodPrintBarcode


__author__ = 'StasEvseev'


blueprint = Blueprint('good_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_canon(GoodResourceCanon, "/good")
api.add_resource(GoodPrintBarcode, "/good/<int:id>/printbarcode")
