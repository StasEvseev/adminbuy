# coding: utf-8

from flask import Blueprint

from adminbuy.resources import MyApi

from .resource import ReceiverResource, ReceiverCanonResource


__author__ = 'StasEvseev'


blueprint = Blueprint('receiver_blueprint', __name__)
api = MyApi(blueprint, prefix='/api')
api.register_canon(ReceiverCanonResource, '/receiver')
