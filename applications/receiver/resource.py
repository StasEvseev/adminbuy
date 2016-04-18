# coding: utf-8

from flask.ext.restful import marshal_with, fields
from applications.receiver.model import Receiver
from applications.receiver.service import ReceiverService

from resources.core import BaseTokeniseResource, BaseCanoniseResource


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
