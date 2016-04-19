# coding: utf-8

from flask import Blueprint

from applications.receiver.resource import ReceiverResource, \
    ReceiverCanonResource
from resources import MyApi

__author__ = 'StasEvseev'


blueprint = Blueprint('receiver_blueprint', __name__)
api = MyApi(blueprint, prefix='/api')
api.register_canon(ReceiverCanonResource, '/receiver')
