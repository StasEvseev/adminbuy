#coding: utf-8

__author__ = 'StasEvseev'

from flask import Blueprint
from applications.collection.resource import CollectCanonResource

from resources import MyApi


blueprint = Blueprint('collect_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_canon(CollectCanonResource, '/collect')