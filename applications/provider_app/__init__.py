#coding: utf-8

__author__ = 'StasEvseev'

from flask import Blueprint

from applications.provider_app.resource import ProviderCanon
from resources import MyApi


blueprint = Blueprint('provider_blueprint', __name__)
api = MyApi(blueprint, prefix='/api')
api.register_canon(ProviderCanon, '/provider')