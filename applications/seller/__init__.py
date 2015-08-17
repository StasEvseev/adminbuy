#coding: utf-8
from flask import Blueprint
from applications.seller.resource import SellerResource

from resources import MyApi


blueprint = Blueprint('seller_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_canon(SellerResource, "/seller")
# api.register_canon(ReturnCanon, '/return')
# api.register_canon(ReturnItemInnerCanon, '/return')

