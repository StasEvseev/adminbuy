#coding: utf-8

__author__ = 'StasEvseev'

from flask.ext.restful import fields
from applications.collection.model import Collect

from applications.commodity.models import Commodity
from resources.core import BaseCanoniseResource


class CollectCanonResource(BaseCanoniseResource):
    model = Collect

    attr_json = {
        'id': fields.Integer,
        'date': fields.String,
        'location_id': fields.Integer,
        'location': fields.Nested({
            'name': fields.String
        }),
        'user_id': fields.Integer,
        'user': fields.Nested({
            'full_name': fields.String
        }),
        'sum': fields.Price,
        'name': fields.String
    }