#coding: utf-8
from functools import wraps
from flask import g
from flask.ext.principal import RoleNeed, Permission, Identity
from flask.ext.restful import fields
from flask.ext.security import roles_accepted, auth_token_required, http_auth_required
from werkzeug.security import generate_password_hash

from applications.security.model import User
from resources.core import BaseCanoniseResource, BaseTokeniseAdminResource
from services.userservice import UserService


def roles_accepted2(*roles):
    """Decorator which specifies that a user must have at least one of the
    specified roles. Example::

        @app.route('/create_post')
        @roles_accepted('editor', 'author')
        def create_post():
            return 'Create Post'

    The current user must have either the `editor` role or `author` role in
    order to view the page.

    :param args: The possible roles.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            g.identity = Identity(g.user.id)
            perm = Permission(*[RoleNeed(role) for role in roles])
            if perm.can():
                return fn(*args, **kwargs)
            return _get_unauthorized_view()
        return decorated_view
    return wrapper


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

    # @roles_accepted(['vendor'])
    # def put(self):
    #     pass
    #
    # @roles_accepted(['vendor'])
    # def post(self, id):
    #     pass

    @roles_accepted2('user')
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