# coding: utf-8

from flask import Blueprint

from adminbuy.resources import MyApi

from .resource import UserCanon, RoleCanon

__author__ = 'StasEvseev'


blueprint = Blueprint('user_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_canon(UserCanon, "/user")
api.register_canon(RoleCanon, "/role")
