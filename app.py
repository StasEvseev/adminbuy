#coding: utf-8

from datetime import timedelta
import os
import time

from flask import Flask, redirect, request, render_template, make_response
from flask.ext.triangle import Triangle
from flask.ext.babel import Babel

from werkzeug.contrib.fixers import ProxyFix

from config import admin_imap, admin_pass, DATABASE_URI, SECRET_KEY

os.environ['TZ'] = 'Europe/Moscow'
# time.tzset()

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

from db import db
from mailmodule import mail
from log import init_logging, debug


def create_app(application):
    from resources import api
    from assets import assets
    from applications.security.auth import login_manager
    from security import security
    # from admin import admin

    application.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    application.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = "AUTHORIZATION"
    application.config['SECURITY_REMEMBER_SALT'] = "SALT123123123"
    # application.config['BABEL_DEFAULT_LOCALE'] = 'ru-ru'
    application.config['SECRET_KEY'] = SECRET_KEY
    application.permanent_session_lifetime = timedelta(minutes=30)

    Triangle(application)
    assets.init_app(application)
    api.init_app(application)
    api.application = application
    db.init_app(application)
    mail.init_app(application)
    login_manager.init_app(application)
    security.init_app(application)

    application.db = db
    application.api = api

    babel = Babel(application)

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(["ru"])

    init_logging(application)

    return application

app = create_app(app)

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
from applications.good_commodity import blueprint as GoodComBl
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
app.register_blueprint(GoodComBl)
app.register_blueprint(SetBl)
app.register_blueprint(OrBl)
app.register_blueprint(ReBl)
app.register_blueprint(WRBl)
app.register_blueprint(SelBl)
app.register_blueprint(ColBl)
app.register_blueprint(UsBl)

app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route('/admin')
def newindex():
    return render_template("index.html")

@app.route('/')
def index():
    return redirect("/admin?%s" % request.query_string)

"""
Сервис воркер(для кеширования страниц и ресурсов в Chrome.
"""
@app.route('/sw.js')
def manifest():
    res = make_response(render_template('sw.js'), 200)
    res.headers["Content-Type"] = "text/javascript"
    return res

@app.route('/update_cache.js')
def update_cache():
    res = make_response(render_template('update_cache.js'), 200)
    res.headers["Content-Type"] = "text/javascript"
    return res


def create_superuser():
    from services.userservice import UserService
    with app.app_context():
        if UserService.check_duplicate('admin'):
            user = UserService.registration('admin', 'a@a.ru', 'admin', is_superuser=True,
                                            first_name='Админов', last_name='Админ', role=['admin'])
            db.session.add(user)
            db.session.commit()
        else:
            raise Exception(u"Has admin.")

app.create_superuser = create_superuser

if __name__ == "__main__":
    debug(u"Запуск системы.")
    app.run(debug=True)


# @app.route('/logout')
# def logout():
#     from flask.ext import login
#     login.logout_user()
#     return redirect(url_for('.login'))
#
#
# @app.route('/login', methods=('GET', 'POST'))
# def login():
#     from flask.ext import login
#     from applications.security.form import LoginForm
#     from flask.ext.admin import helpers
#     form = LoginForm(request.form)
#     if helpers.validate_form_on_submit(form):
#         user = form.get_user()
#         login.login_user(user)
#         from flask import session
#         session.permanent = True
#
#     if login.current_user.is_authenticated():
#         if 'target' in request.args:
#             return redirect(request.args['target'])
#         return redirect(url_for('newindex'))
#     # link = u'<p>Не имеете аккаунта? <a id="a_reg" href="' + url_for('.register_view') + u'">Нажмите для регистрации.</a></p>'
#     # self._template_args['form'] = form
#     # self._template_args['link'] = link
#     return render_template("newadmin/login.html")