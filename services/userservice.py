from werkzeug.security import generate_password_hash

from applications.security.model import User
from applications.settings.model import Profile

from services.core import BaseSQLAlchemyModelService

from itsdangerous import JSONWebSignatureSerializer as Serializer

from config import SECRET_KEY


class UserService(BaseSQLAlchemyModelService):
    model = User

    @classmethod
    def check_duplicate(cls, login, email, id=None):
        query = cls.model.query.filter_by(login=login)
        if id:
            query = query.filter(id!=id)
        if query.count() > 0:
            return False
        return True

    @classmethod
    def registration(cls, login, email, password, is_superuser=False, first_name=None, last_name=None):
        user = cls.create_instance(login=login, email=email, password=generate_password_hash(password),
                                   is_superuser=is_superuser, first_name=first_name, last_name=last_name)
        profile = Profile()
        profile.user = user
        return user

    @classmethod
    def user_to_token(cls, token):
        id = cls._get_id_from_token(token)
        return cls.get_by_id(id)

    @classmethod
    def _get_id_from_token(cls, token):
        s = Serializer(SECRET_KEY)
        d = s.loads(token)
        return d['id']