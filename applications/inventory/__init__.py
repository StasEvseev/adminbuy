# coding: utf-8

from flask import Blueprint

from applications.inventory.resource import (
    InventoryCanon, InventoryStatusResource, InventoryItemCanon,
    InventoryItemInnerCanon, InventoryPrint)
from resources import MyApi

__author__ = 'StasEvseev'


blueprint = Blueprint('inventory_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_canon(InventoryCanon, '/inventory')
api.register_canon(InventoryItemInnerCanon, '/inventory')
api.register_canon(InventoryItemCanon, '/inventory-items')
api.add_resource(InventoryStatusResource, '/inventory/<int:id>/status')
api.add_resource(InventoryPrint, '/inventory/print/<int:id>')
