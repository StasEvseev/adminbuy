#coding: utf-8

__author__ = 'StasEvseev'

from flask.ext.restful import fields

from applications.provider_app.models import Provider
from resources.core import BaseCanoniseResource


class ProviderCanon(BaseCanoniseResource):

    model = Provider
    attr_json = {
        'id': fields.Integer,
        'name': fields.String,
        'address': fields.String,
        'emails': fields.String
    }

    multif = {'filter_field': ('name', 'address')}