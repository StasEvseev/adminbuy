# coding: utf-8

from flask import Blueprint
from resources import MyApi
from applications.security.resource import UserCanon, RoleCanon


blueprint = Blueprint('user_blueprint', __name__)

api = MyApi(blueprint, prefix='/api')
api.register_canon(UserCanon, "/user")
api.register_canon(RoleCanon, "/role")
