#coding: utf-8
from flask.ext.login import current_user
from flask.ext.principal import identity_loaded, UserNeed
from flask.ext.security import SQLAlchemyUserDatastore
from flask.ext.security import Security
from db import db

__author__ = 'Stanislav'

from applications.security.model import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)