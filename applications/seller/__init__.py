# coding: utf-8

from flask import Blueprint
from applications.seller.resource import SellerResource

from resources import MyApi

__author__ = 'StasEvseev'


blueprint = Blueprint('seller_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_canon(SellerResource, "/seller")
