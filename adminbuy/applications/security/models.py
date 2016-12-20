# coding: utf-8

from flask.ext.security import RoleMixin, UserMixin
from flask.ext.security.core import _token_loader
from werkzeug.security import check_password_hash

from adminbuy.db import db


__author__ = 'StasEvseev'


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
    useexisting=True
)


class Role(db.Model, RoleMixin):
    __table_args__ = {'useexisting': True}

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __table_args__ = {'useexisting': True}

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120))
    password = db.Column(db.String)
    is_superuser = db.Column(db.Boolean, default=False)
    roles = db.relationship(
        Role, secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'))
    active = db.Column(db.Boolean, default=True)

    @property
    def full_name(self):
        return " ".join([self.first_name or "", self.last_name or ""])

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self):
        return self.get_auth_token()

    @staticmethod
    def verify_auth_token(token):
        res = _token_loader(token)
        if ((callable(res.is_anonymous) and res.is_anonymous()) or
                (not callable(res.is_anonymous) and res.is_anonymous)):
            res = None
        return res

    # Required for administrative interface
    def __unicode__(self):
        return self.login
