# coding: utf-8

from flask import Blueprint

from adminbuy.resources import MyApi

from .resource import PointSaleCanon, PointSaleItemInnerCanon


__author__ = 'StasEvseev'


blueprint = Blueprint('pointsale_blueprint', __name__)
api = MyApi(blueprint, prefix='/api')

api.register_canon(PointSaleCanon, '/pointsale')
api.register_canon(PointSaleItemInnerCanon, '/pointsale')
