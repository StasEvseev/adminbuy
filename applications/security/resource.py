#coding: utf-8
from flask.ext.restful import fields

from werkzeug.security import generate_password_hash
from applications.security.decorators import roles_accepted2

from applications.security.model import User, Role
from db import db
from resources.core import BaseCanoniseResource, BaseTokeniseAdminResource
from security import user_datastore
from services.userservice import UserService


class RoleCanon(BaseCanoniseResource):
    model = Role

    base_class = BaseTokeniseAdminResource

    attr_json = {
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String,
    }


class UserCanon(BaseCanoniseResource):

    class UserCanonExc(BaseCanoniseResource.CanonException):
        pass

    model = User

    base_class = BaseTokeniseAdminResource

    attr_json = {
        'id': fields.Integer,
        'first_name': fields.String,
        'last_name': fields.String,
        'login': fields.String,
        'email': fields.String,
        'is_superuser': fields.Boolean,
        'roles': fields.Nested({
            'id': fields.Integer,
            'name': fields.String,
            'description': fields.String
        }),
        'active': fields.Boolean
    }

    def pre_save(self, obj, data):
        if obj.id is None:
            password = data.get('password')
            retypepassword = data.get('retypepassword')
            if password is None or retypepassword is None:
                raise UserCanon.UserCanonExc(u"Не заполнены пароли.")
            if password != retypepassword:
                raise UserCanon.UserCanonExc(u"Пароли не совпадают!")
            obj.password = password

        roles = data.get('roles')

        login = data.get('login')
        email = data.get('email')

        if login is None or email is None:
            raise UserCanon.UserCanonExc(u"Не заполнены логин или почтовый ящик.")

        if not roles:
            raise UserCanon.UserCanonExc(u"Не выбраны роли для пользователя.")
        obj._roles = [x['name'] for x in roles]

        if not UserService.check_duplicate(login, email, id):
            raise UserCanon.UserCanonExc(u"В системе уже есть запись с именем '%s'" % login)
        return obj

    def save_model(self, obj):
        if obj.id is None:
            return UserService.registration(
                obj.login, obj.email, obj.password, obj.is_superuser, obj.first_name, obj.last_name, obj._roles)
        _roles = [role.name for role in obj.roles]

        for rol in list(set(_roles).difference(obj._roles)):
            user_datastore.remove_role_from_user(obj, rol)
        for rol in list(set(obj._roles).difference(_roles)):
            user_datastore.add_role_to_user(obj, rol)

        db.session.add(obj)
        return obj