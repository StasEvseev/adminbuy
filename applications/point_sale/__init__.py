#coding: utf-8

__author__ = 'StasEvseev'

from flask import Blueprint

from applications.point_sale.resource import PointSaleItemInnerCanon, PointSaleCanon#, PointSaleItemResource
from resources import MyApi


blueprint = Blueprint('pointsale_blueprint', __name__)
api = MyApi(blueprint, prefix='/api')

api.register_canon(PointSaleCanon, '/pointsale')
api.register_canon(PointSaleItemInnerCanon, '/pointsale')