# coding: utf-8

import os

try:
    from config_local import USER
    from config_local import PASSWORD
except ImportError:
    USER = 'adminbuy'
    PASSWORD = 'adminbuy'

DB = 'adminbuy'

IS_PROD = False

try:
    from config_local import IS_PROD
except ImportError:
    pass

COMMON_URL = 'postgresql://%s:%s@localhost:5432/%s'

DATABASE_URI = COMMON_URL % (USER, PASSWORD, DB)

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
    admin_imap = ""
    admin_pass = ""

try:
    from config_local import ADMINS
except ImportError:
    ADMIN = "stasevseev@gmail.com"
    ADMINS = [ADMIN]


__author__ = 'StasEvseev'


imap_server = 'imap.gmail.com'


DIR_PROJECT = os.path.dirname(__file__)
DIR_ALEMBIC = os.path.join(DIR_PROJECT, 'adminbuy', 'migrations')
mail_folder = 'attachments'

PATH_TO_GENERATE_INVOICE = os.path.join(DIR_PROJECT, 'static', 'files')
PATH_WEB = "/" + os.path.join('static', 'files')

PATH_TO_ANGULAR_APPS = os.path.join(
    DIR_PROJECT, 'static', 'newadmin', 'js', 'applications')
