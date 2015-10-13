#coding: utf-8

__author__ = 'StasEvseev'


import os
import unittest
import sys
from flask import json
import psycopg2
import app
from config import COMMON_URL, USER, PASSWORD, DB
from manage import man

CURRENT_DIR = os.path.dirname(__file__)
PATH_DB = os.path.join(CURRENT_DIR, "app.db")


def initializetest(app):
    # with app.app_context():
        # print the connection string we will use to connect
        # print "Connecting to database\n	->%s" % (conn_string)

        # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(COMMON_URL % (USER, PASSWORD, DB))
    with conn.cursor() as cur:
        conn.autocommit = True
        conn.set_isolation_level(0)
        cur.execute("DROP DATABASE IF EXISTS test;")
        cur.execute("CREATE DATABASE test;")
        conn.commit()

    app.config['SQLALCHEMY_DATABASE_URI'] = COMMON_URL % (USER, PASSWORD, "test")
    app.config['TESTING'] = True

    old_argv = sys.argv
    sys.argv = []
    sys.argv.append("manage.py")
    sys.argv.append("db")
    sys.argv.append("upgrade")

    man.run()

    sys.argv = old_argv


class BaseTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(BaseTestCase, self).__init__(*args, **kwargs)

        self.module = app
        self.application = self.module.app

    def setUp(self):
        initializetest(self.application)

        self.client = self.application.test_client()

        self.__initialize()

        self.set_up()

    def __initialize(self):
        """
        Инициализация БД. Нужен как минимум один пользователь.
        """

        from services.userservice import UserService
        from db import db

        with self.application.app_context():
            user = UserService.registration('I', 'a@a2.ru', 'I')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        self.tear_down()
        with app.app.app_context():
            app.app.db.engine.dispose()

    def _serialize(self, dict):
        return json.dumps(dict)

    def _deserialize(self, data):
        return json.loads(data)

    def set_up(self):
        pass

    def tear_down(self):
        pass


class BaseLiveTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseLiveTestCase, self).__init__(*args, **kwargs)

        self.module = app
        self.application = self.module.app

    def setUp(self):

        self.set_up()

    def tearDown(self):
        self.tear_down()
        with app.app.app_context():
            app.app.db.engine.dispose()

    def set_up(self):
        pass

    def tear_down(self):
        pass