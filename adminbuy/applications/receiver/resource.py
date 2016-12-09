# coding: utf-8

from flask.ext.restful import marshal_with, fields

from adminbuy.resources.core import BaseTokeniseResource, BaseCanoniseResource

from .model import Receiver
from .service import ReceiverService


__author__ = 'StasEvseev'


class ReceiverResource(BaseTokeniseResource):
    @marshal_with({'items': fields.List(fields.Nested({
        'id': fields.Integer,
        'fullname': fields.String,
        'fname': fields.String,
        'lname': fields.String,
        'pname': fields.String,
        'address': fields.String,
        'passport': fields.String
    }))})
    def get(self):
        return {'items': ReceiverService.get_all()}


class ReceiverCanonResource(BaseCanoniseResource):
    model = Receiver

    attr_json = {
        'id': fields.Integer,
        'fullname': fields.String,
        'fname': fields.String,
        'lname': fields.String,
        'pname': fields.String,
        'address': fields.String,
        'passport': fields.String
    }
