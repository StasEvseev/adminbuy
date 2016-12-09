# coding: utf-8

from flask.ext.restful import fields

from adminbuy.resources.core import BaseCanoniseResource

from .models import Provider


__author__ = 'StasEvseev'


class ProviderCanon(BaseCanoniseResource):

    model = Provider
    attr_json = {
        'id': fields.Integer,
        'name': fields.String,
        'address': fields.String,
        'emails': fields.String
    }

    multif = {'filter_field': ('name', 'address')}
