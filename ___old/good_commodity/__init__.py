#coding: utf-8

__author__ = 'StasEvseev'

from flask import Blueprint

from ___old.good_commodity import GoodCommodityResource
from resources import MyApi

blueprint = Blueprint('goodcommodity_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_getall(GoodCommodityResource, '/good/tocommodity/<int:id>')