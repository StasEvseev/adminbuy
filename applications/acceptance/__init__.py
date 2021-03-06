# coding: utf-8

from flask import Blueprint
from applications.acceptance.resource import AcceptanceCanon, \
    AcceptanceItemsResource, AcceptanceRemainItemsResource, \
    AcceptanceStatusResource, AcceptanceItemInnerCanon

from resources import MyApi


blueprint = Blueprint(
    'acceptance_blueprint', __name__, static_folder='static',
    template_folder='templates', static_url_path='/static/acceptance')

api = MyApi(blueprint, prefix='/api')
api.register_canon(AcceptanceCanon, '/acceptance')
api.register_canon(AcceptanceItemInnerCanon, '/acceptance')
api.add_resource(AcceptanceStatusResource, '/acceptance/<int:id>/status')
