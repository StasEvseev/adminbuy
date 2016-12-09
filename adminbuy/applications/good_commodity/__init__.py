# coding: utf-8

from flask import Blueprint

from adminbuy.resources import MyApi

from .resource import GoodCommodityResource


blueprint = Blueprint('goodcommodity_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_getall(GoodCommodityResource, '/good/tocommodity/<int:id>')
