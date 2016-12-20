# coding: utf-8

from flask import Blueprint

from adminbuy.resources import MyApi

from adminbuy.applications.provider_app.resource import ProviderCanon


__author__ = 'StasEvseev'


blueprint = Blueprint('provider_blueprint', __name__)
api = MyApi(blueprint, prefix='/api')
api.register_canon(ProviderCanon, '/provider')
