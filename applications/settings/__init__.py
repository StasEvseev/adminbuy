#coding: utf-8

from flask import Blueprint

from applications.settings.resource import ProfileCanon
from resources import MyApi


blueprint = Blueprint('settings_blueprint', __name__)
api = MyApi(blueprint, prefix='/api')

api.register_canon(ProfileCanon, '/settings')

# api.register_canon(PointSaleCanon, '/pointsale')
# api.register_canon(PointSaleItemInnerCanon, '/pointsale')