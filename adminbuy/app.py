# coding: utf-8

import os
from datetime import timedelta

from flask import Flask, render_template
from flask.ext.triangle import Triangle

from werkzeug.contrib.fixers import ProxyFix

from db import db
from log import init_logging, debug

from config import admin_imap, admin_pass, DATABASE_URI, SECRET_KEY, IS_PROD


__author__ = 'StasEvseev'


os.environ['TZ'] = 'Europe/Moscow'


def create_app():
    app = Flask(__name__)
    app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379/0',
        CELERY_RESULT_BACKEND='redis://localhost:6379/0'
    )
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = admin_imap
    app.config['MAIL_PASSWORD'] = admin_pass
    app.config['MAIL_DEFAULT_SENDER'] = 'server-error@example.com'

    return app


def init_app(application):
    from resources import api
    from assets import assets
    from applications.security.auth import login_manager
    from security import security

    application.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    application.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = (
        "AUTHORIZATION")
    application.config['SECURITY_REMEMBER_SALT'] = "SALT123123123"
    application.config['SQLALCHEMY_ECHO'] = True
    application.config['SECRET_KEY'] = SECRET_KEY
    application.permanent_session_lifetime = timedelta(minutes=30)

    Triangle(application)

    assets.init_app(application)
    api.init_app(application)
    api.application = application

    db.init_app(application)
    login_manager.init_app(application)
    security.init_app(application)

    application.db = db
    application.api = api

    if IS_PROD:
        init_logging(application)

    return application


def initialize_blueprints(app):
    from applications.commodity import blueprint as ComBl
    from applications.point_sale import blueprint as PSBl
    from applications.inventory import blueprint as InvBl
    from applications.provider_app import blueprint as PrBl
    from applications.waybill import blueprint as WbBl
    from applications.acceptance import blueprint as AcBl
    from applications.receiver import blueprint as RcBl
    from applications.good import blueprint as GdBl
    from applications.invoice import blueprint as InBl
    from applications.price import blueprint as PriceBl
    from applications.settings import blueprint as SetBl
    from applications.order import blueprint as OrBl
    from applications.return_app import blueprint as ReBl
    from applications.waybill_return import blueprint as WRBl
    from applications.seller import blueprint as SelBl
    from applications.collection import blueprint as ColBl
    from applications.security.bl import blueprint as UsBl

    app.register_blueprint(ComBl)
    app.register_blueprint(PSBl)
    app.register_blueprint(InvBl)
    app.register_blueprint(PrBl)
    app.register_blueprint(WbBl)
    app.register_blueprint(AcBl)
    app.register_blueprint(RcBl)
    app.register_blueprint(GdBl)
    app.register_blueprint(InBl)
    app.register_blueprint(PriceBl)
    app.register_blueprint(SetBl)
    app.register_blueprint(OrBl)
    app.register_blueprint(ReBl)
    app.register_blueprint(WRBl)
    app.register_blueprint(SelBl)
    app.register_blueprint(ColBl)
    app.register_blueprint(UsBl)

    app.wsgi_app = ProxyFix(app.wsgi_app)

    return app

app = create_app()
app = init_app(app)
app = initialize_blueprints(app)


@app.route('/admin/')
def newindex():
    return render_template("index.html")


@app.route('/')
def index():
    return render_template('home.html')


# commands
def create_superuser():
    from services.userservice import UserService
    with app.app_context():
        if UserService.check_duplicate('admin'):
            user = UserService.registration(
                'admin', 'a@a.ru', 'admin', is_superuser=True,
                first_name='Админов', last_name='Админ', role=['admin'])
            db.session.add(user)
            db.session.commit()
        else:
            debug(u'Error - has admin.')
            raise Exception(u"Has admin.")


def change_password(username, password):
    from services.userservice import UserService

    with app.app_context():
        user = UserService.change_password(username, password)

        db.session.add(user)
        db.session.commit()


app.create_superuser = create_superuser
app.change_password = change_password

if __name__ == "__main__":
    debug(u"Запуск системы.")
    app.run(debug=True)
