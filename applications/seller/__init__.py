#coding: utf-8

__author__ = 'StasEvseev'

from flask import Blueprint
from applications.seller.resource import SellerResource

from resources import MyApi


blueprint = Blueprint('seller_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_canon(SellerResource, "/seller")
