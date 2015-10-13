#coding: utf-8

__author__ = 'StasEvseev'

from flask import Blueprint
from applications.order.resource import OrderCanon, OrderItemInnerCanon

from resources import MyApi


blueprint = Blueprint('order_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_canon(OrderCanon, '/order')
api.register_canon(OrderItemInnerCanon, '/order')
