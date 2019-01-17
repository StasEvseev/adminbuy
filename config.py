# coding: utf-8

__author__ = 'StasEvseev'

import os

try:
    from config_local import USER
    from config_local import PASSWORD
    from config_local import DB
    from config_local import DB_HOST
except ImportError:
    USER = 'buyapi'
    PASSWORD = 'buyapi'
    DB = 'buyapi'
    DB_HOST = 'localhost'

IS_PROD = False

try:
    from config_local import IS_PROD
except ImportError:
    pass

if IS_PROD:
    API_LOCATION = 'https://evfam.com/v2/api'
else:
    API_LOCATION = 'http://127.0.0.1:8000/api'

COMMON_URL = 'postgresql://%s:%s@%s:5432/%s'

DATABASE_URI = COMMON_URL % (USER, PASSWORD, DB_HOST, DB)

try:
    from config_local import SECRET_KEY
except ImportError:
    SECRET_KEY = 'test'

try:
    from config_local import user_imap
    from config_local import user_pass
except ImportError:
    user_imap = ''
    user_pass = ''

try:
    from config_local import admin_imap
    from config_local import admin_pass
except ImportError:
    admin_imap = ''
    admin_pass = ''

try:
    from config_local import ADMINS
except ImportError:
    ADMIN = 'stasevseev@gmail.com'
    ADMINS = [ADMIN]

imap_server = 'imap.gmail.com'


DIR_PROJECT = os.path.dirname(__file__)
mail_folder = 'attachments'

PATH_TO_GENERATE_INVOICE = os.path.join(DIR_PROJECT, 'static_foreign', 'files')
PATH_WEB = "/" + os.path.join('static', 'files')

PATH_TO_ANGULAR_APPS = os.path.join(
    DIR_PROJECT, 'static', 'newadmin', 'js', 'applications')
