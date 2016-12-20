# coding: utf-8

from flask import Blueprint

from adminbuy.resources import MyApi

from adminbuy.applications.order.resource import OrderCanon, OrderItemInnerCanon


__author__ = 'StasEvseev'


blueprint = Blueprint('order_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_canon(OrderCanon, '/order')
api.register_canon(OrderItemInnerCanon, '/order')
