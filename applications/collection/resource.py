#coding: utf-8
from flask.ext.restful import fields
from applications.collection.model import Collect

from applications.commodity.models import Commodity
from resources.core import BaseCanoniseResource


class CollectCanonResource(BaseCanoniseResource):
    model = Collect

    # multif = {'filter_field': ('name', 'thematic')}

    attr_json = {
        'id': fields.Integer,
        'date': fields.String,
        'location_id': fields.Integer,
        'location': fields.Nested({
            'name': fields.String
        }),
        'seller_id': fields.Integer,
        'seller': fields.Nested({
            'fullname': fields.String
        }),
        'sum': fields.Price,
        'name': fields.String
    }