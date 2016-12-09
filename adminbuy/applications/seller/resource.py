# coding: utf-8

from flask.ext.restful import fields

from adminbuy.resources.core import BaseCanoniseResource

from .model import Seller


__author__ = 'StasEvseev'


class SellerResource(BaseCanoniseResource):
    model = Seller
    attr_json = {
        'id': fields.Integer,
        'fname': fields.String,
        'lname': fields.String,
        'pname': fields.String,
        'address': fields.String,
        'passport': fields.String,
        'fullname': fields.String,
    }
