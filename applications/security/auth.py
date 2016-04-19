# coding: utf-8

from flask import make_response, jsonify, g
from flask.ext import login
from flask.ext.httpauth import HTTPBasicAuth

from db import db
from model import User

__author__ = 'StasEvseev'


auth = HTTPBasicAuth()
auth_admin = HTTPBasicAuth()

login_manager = login.LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


def unauthorized():
    return make_response(
        jsonify({'error': 'Unauthorized access'}), 401,
        [('WWW-Authenticate', 'error')])


def access_denied():
    return make_response(
        jsonify({'error': "Permission denied"}), 403,
        [('WWW-Authenticate', 'error')])


auth.error_handler(unauthorized)

auth_admin.error_handler(access_denied)


def verify(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(login=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


def verify_admin(username, password):
    user = User.verify_auth_token(username)

    if not user:
        user = User.query.filter_by(login=username).first()
        if not user or not user.verify_password(password):
            return False

    if user.is_superuser:
        g.user = user
        return True
    return False


auth.verify_password(verify)
auth_admin.verify_password(verify_admin)
