# coding: utf-8

from werkzeug.security import generate_password_hash

from applications.security.model import User
from applications.settings.model import Profile
from security import user_datastore

from services.core import BaseSQLAlchemyModelService


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
    def change_password(cls, login, password):

        if cls.check_duplicate(login):
            raise UserService.DuplicateError(
                u"В системе нет пользователя с логином - '%s'" % login)

        user = cls.get_by_name(login)

        user.password = generate_password_hash(password)

        return user

    @classmethod
    def registration(cls, login, email, password, is_superuser=False,
                     first_name=None, last_name=None, role=None):
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
            raise UserService.DuplicateError(
                u"В системе есть пользователь с логином - '%s'" % login)

        role = role or ['user']
        user = user_datastore.create_user(
            login=login, email=email, is_superuser=is_superuser,
            password=generate_password_hash(password), first_name=first_name,
            last_name=last_name, roles=role)
        profile = Profile()
        profile.user = user

        return user

    @classmethod
    def user_to_token(cls, token):
        user = User.verify_auth_token(token)

        return user
