# coding: utf-8

from flask import Blueprint

from adminbuy.resources import MyApi
from adminbuy.applications.settings.resource import ProfileCanon

__author__ = 'StasEvseev'


blueprint = Blueprint('settings_blueprint', __name__)
api = MyApi(blueprint, prefix='/api')

api.register_canon(ProfileCanon, '/settings')
