#coding: utf-8

import os
import unittest
import sys
from flask import json
import psycopg2
import app
from config import COMMON_URL, USER, PASSWORD, DB
from db import db
from manage import man

CURRENT_DIR = os.path.dirname(__file__)
PATH_DB = os.path.join(CURRENT_DIR, "app.db")

import sqlalchemy.event.base
# class mCl(ConnectionEventsDispatch):
# <sqlalchemy.event.base.ConnectionEventsDispatch object at 0x7f02340e0210>
#     pass


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
        data = self.application.test_client().post("/admin/register/", data={
            'login': 'I',
            'email': 'a@a2.ru',
            'password': 'I'
        }, follow_redirects=True)
        assert data.status_code, 200
        # assert "Добро пожаловать!" in data.data

    def tearDown(self):



        # with app.app.app_context():
        #     db.drop_all()
        # os.remove(PATH_DB)

        self.tear_down()
        with app.app.app_context():
            app.app.db.engine.dispose()
            # app.app.db.engine.pool.recreate()
        # app.db.

    def _serialize(self, dict):
        return json.dumps(dict)

    def _deserialize(self, data):
        return json.loads(data)

    def set_up(self):
        pass

    def tear_down(self):
        pass