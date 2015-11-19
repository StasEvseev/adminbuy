# coding: utf-8

from flask.ext.security import SQLAlchemyUserDatastore
from flask.ext.security import Security

from db import db

from applications.security.model import User, Role

__author__ = 'StasEvseev'


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)
