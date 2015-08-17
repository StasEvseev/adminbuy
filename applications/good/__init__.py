#coding: utf-8
from flask import Blueprint


from resources import MyApi
from applications.good.resource import GoodResourceCanon


blueprint = Blueprint('good_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_canon(GoodResourceCanon, "/good")