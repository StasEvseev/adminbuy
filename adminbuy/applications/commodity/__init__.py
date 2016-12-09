# coding: utf-8

from flask import Blueprint

from adminbuy.resources import MyApi

from .resource import CommodityCanonResource
from .service import CommodityService

__author__ = 'StasEvseev'


blueprint = Blueprint('commodity_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_canon(CommodityCanonResource, '/commodity')
