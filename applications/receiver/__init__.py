#coding: utf-8

__author__ = 'StasEvseev'

from flask import Blueprint

from applications.receiver.resource import ReceiverResource, ReceiverCanonResource
from resources import MyApi


blueprint = Blueprint('receiver_blueprint', __name__)
api = MyApi(blueprint, prefix='/api')
api.register_canon(ReceiverCanonResource, '/receiver')

