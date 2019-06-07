# coding: utf-8

__author__ = 'StasEvseev'

import os

USER = 'buyapi'
PASSWORD = 'buyapi'
DB = 'buyapi'
DB_HOST = 'localhost'

IS_PROD = False

ADMIN = 'stasevseev@gmail.com'
ADMINS = [ADMIN]

SECRET_KEY = 'test'

user_imap = ''
user_pass = ''

admin_imap = ''
admin_pass = ''
imap_server = 'imap.gmail.com'


if IS_PROD:
    API_LOCATION = 'https://evfam.com/v2/api'
else:
    API_LOCATION = 'http://127.0.0.1:8000/api'

if 'API_LOCATION' in os.environ:
    API_LOCATION = os.environ.get('API_LOCATION')

from config_local import *

COMMON_URL = 'postgresql://%s:%s@%s:5432/%s'

DATABASE_URI = COMMON_URL % (USER, PASSWORD, DB_HOST, DB)


DIR_PROJECT = os.path.dirname(__file__)
mail_folder = 'attachments'

PATH_TO_GENERATE_INVOICE = os.path.join(DIR_PROJECT, 'static_foreign', 'files')
PATH_WEB = "/" + os.path.join('static', 'files')

PATH_TO_ANGULAR_APPS = os.path.join(
    DIR_PROJECT, 'static', 'newadmin', 'js', 'applications')
