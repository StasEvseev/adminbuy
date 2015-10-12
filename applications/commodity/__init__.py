#coding: utf-8
from flask import Blueprint
from flask.ext.injector import FlaskInjector
from injector import Key

from resources import MyApi
from applications.commodity.resource import CommodityCanonResource
from applications.commodity.service import CommodityService


blueprint = Blueprint('commodity_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_canon(CommodityCanonResource, '/commodity')


def configure(binder):
    print "commodity configure"
    binder.bind(Key('CommodityService'), CommodityService)