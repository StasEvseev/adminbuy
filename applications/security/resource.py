#coding: utf-8
from flask.ext.restful import fields

from werkzeug.security import generate_password_hash
from applications.security.decorators import roles_accepted2

from applications.security.model import User, Role
from resources.core import BaseCanoniseResource, BaseTokeniseAdminResource
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
        'is_superuser': fields.Boolean
    }

    def pre_save(self, obj, data):
        if obj.id is None:
            password = data.get('password')
            retypepassword = data.get('retypepassword')
            if password is None or retypepassword is None:
                raise UserCanon.UserCanonExc(u"Не заполнены пароли.")
            if password != retypepassword:
                raise UserCanon.UserCanonExc(u"Пароли не совпадают!")
            obj.password = generate_password_hash(password)

        login = data.get('login')
        email = data.get('email')

        if login is None or email is None:
            raise UserCanon.UserCanonExc(u"Не заполнены логин или почтовый ящик.")

        if not UserService.check_duplicate(login, email, id):
            raise UserCanon.UserCanonExc(u"В системе уже есть запись с именем '%s'" % login)
        return obj