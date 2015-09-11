#coding: utf-8
from flask.ext.security import RoleMixin, UserMixin
from flask.ext.security.core import _token_loader
from flask.ext.security.passwordless import generate_login_token, login_token_status
from db import db

from config import SECRET_KEY

from itsdangerous import JSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

from werkzeug.security import check_password_hash


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120))
    password = db.Column(db.String)
    is_superuser = db.Column(db.Boolean, default=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self):
        # s = Serializer(SECRET_KEY)
        return self.get_auth_token()
        # return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        res = _token_loader(token)
        if res.is_anonymous():
            res = None
        return res
        # expired, invalid, user = login_token_status(token)
        # return user

    # Required for administrative interface
    def __unicode__(self):
        return self.login