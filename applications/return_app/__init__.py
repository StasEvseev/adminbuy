#coding: utf-8

__author__ = 'StasEvseev'

from flask import Blueprint
from applications.return_app.resource import ReturnCanon, ReturnItemInnerCanon, ReturnStatusResource

from resources import MyApi


blueprint = Blueprint('return_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_canon(ReturnCanon, '/return')
api.register_canon(ReturnItemInnerCanon, '/return')
api.add_resource(ReturnStatusResource, '/return/<int:id>/status')