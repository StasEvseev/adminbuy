# coding: utf-8

from flask import Blueprint

from adminbuy.resources import MyApi

from .resource import SellerResource


__author__ = 'StasEvseev'


blueprint = Blueprint('seller_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_canon(SellerResource, "/seller")
