#coding: utf-8

__author__ = 'StasEvseev'

from flask.ext.security import SQLAlchemyUserDatastore
from flask.ext.security import Security
from db import db

from applications.security.model import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)