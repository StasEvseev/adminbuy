#coding: utf-8
from werkzeug.security import generate_password_hash

from applications.security.model import User
from applications.settings.model import Profile
from security import user_datastore

from services.core import BaseSQLAlchemyModelService

from itsdangerous import JSONWebSignatureSerializer as Serializer

from config import SECRET_KEY


class UserService(BaseSQLAlchemyModelService):
    model = User

    class DuplicateError(BaseSQLAlchemyModelService.ServiceException):
        pass

    @classmethod
    def has_by_name(cls, username):
        query = cls.model.query.filter_by(login=username)
        return query.count() > 0

    @classmethod
    def get_by_name(cls, username):
        if cls.has_by_name(username):
            return cls.model.query.filter_by(login=username)[0]
        return None

    @classmethod
    def check_duplicate(cls, login, email=None, id=None):
        query = cls.model.query.filter_by(login=login)
        if id:
            query = query.filter(id!=id)
        if query.count() > 0:
            return False
        return True

    @classmethod
    def registration(cls, login, email, password, is_superuser=False, first_name=None, last_name=None, role=None):
        """
        регистрация пользователя в системе

        :param login - логин
        :param email
        :param password
        :param is_superuser
        :param first_name
        :param last_name
        :param role - роли в системе (список строк ролей)

        :return User
        """

        if not cls.check_duplicate(login):
            raise UserService.DuplicateError(u"В системе есть пользователь с логином - '%s'" % login)

        role = role or ['user']
        user = user_datastore.create_user(
            login=login, email=email, password=generate_password_hash(password),
            is_superuser=is_superuser, first_name=first_name, last_name=last_name, roles=role)
        profile = Profile()
        profile.user = user
        return user

    @classmethod
    def user_to_token(cls, token):
        user = User.verify_auth_token(token)
        return user