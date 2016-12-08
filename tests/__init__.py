# coding: utf-8

import os
import unittest
import sys

import psycopg2

from flask import json

from config import COMMON_URL, USER, PASSWORD, DB

from management import man

from app import app
from db import db

__author__ = 'StasEvseev'

CURRENT_DIR = os.path.dirname(__file__)
PATH_DB = os.path.join(CURRENT_DIR, "app.db")


def initializetest(app):
    conn = psycopg2.connect(COMMON_URL % (USER, PASSWORD, DB))
    with conn.cursor() as cur:
        conn.autocommit = True
        conn.set_isolation_level(0)
        cur.execute("DROP DATABASE IF EXISTS test;")
        cur.execute("CREATE DATABASE test;")
        conn.commit()

    app.config['SQLALCHEMY_DATABASE_URI'] = COMMON_URL % (
        USER, PASSWORD, "test")
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
        unittest.TestCase.__init__(self, *args, **kwargs)

        self.application = app
        self.db = db

    def setUp(self):
        super(BaseTestCase, self).setUp()
        initializetest(self.application)

        self.client = self.application.test_client()

        self.__initialize()

        self.set_up()

    def __initialize(self):
        """
        Инициализация БД. Нужен как минимум один пользователь.
        """

        from services.userservice import UserService

        with self.application.app_context():
            user = UserService.registration('I', 'a@a2.ru', 'I')
            self.db.session.add(user)
            self.db.session.commit()

    def tearDown(self):
        super(BaseTestCase, self).tearDown()

        self.tear_down()
        with app.app_context():
            self.db.engine.dispose()

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

        self.application = app
        self.db = db

    def setUp(self):

        self.set_up()

    def tearDown(self):
        self.tear_down()
        with self.application.app_context():
            self.db.engine.dispose()

    def set_up(self):
        pass

    def tear_down(self):
        pass
