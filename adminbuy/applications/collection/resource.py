# coding: utf-8

from flask.ext.restful import fields

from adminbuy.resources.core import BaseCanoniseResource

from .model import Collect


__author__ = 'StasEvseev'


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
