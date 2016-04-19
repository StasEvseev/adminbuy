# coding: utf-8

from flask.ext.restful import fields
from applications.seller.model import Seller
from resources.core import BaseCanoniseResource

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
