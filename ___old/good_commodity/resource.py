#coding: utf-8

__author__ = 'StasEvseev'

from flask.ext.restful import fields
from applications.good.model import Good
from resources.core import GetResource


class GoodCommodityResource(GetResource):
    model = Good

    attr_json = {
        'id': fields.Integer,
        'full_name': fields.String,
        'commodity_id': fields.Integer,
        'number_local': fields.String,
        'number_global': fields.String,
        'barcode': fields.String,
        'price_id': fields.Integer(default=None),
        'price': fields.Nested({
            'id': fields.Integer,
            'price_gross': fields.String,
            'price_retail': fields.String
        }),
    }

    def query_initial(self, *args, **kwargs):
        return self.model.query.filter(
            self.model.commodity_id == kwargs['id']
        )