# coding: utf-8

from adminbuy.app import app
from adminbuy.management import manager

__author__ = 'StasEvseev'


class TestConfig(object):
    # SQLALCHEMY_DATABASE_URI = 'sqlite://'
    testing = True
    debug = True
    FIXTURES_DIRS = ['datas/fixtures']

app.config.from_object(TestConfig)


if __name__ == "__main__":
    manager.run()
