#coding: utf-8

__author__ = 'StasEvseev'

from flask import url_for, redirect, request
from flask.ext import admin, login
from flask.ext.admin import expose, helpers
from werkzeug.security import generate_password_hash

from applications.security.model import User
from applications.security.form import LoginForm, RegistrationForm
from applications.settings.model import Profile
from db import db


class MyAdminIndexView(admin.AdminIndexView):
    """
    Базовая вьюха админки
    """

    def get_id(self):
        return self.__class__.__name__.lower()

    def is_visible(self):
        return False

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('.login_view') + "?" + request.query_string)
        self.name = u"Главная"
        return super(MyAdminIndexView, self).index()

    @expose('/login', methods=('GET', 'POST'))
    def login_view(self):
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)
            from flask import session
            session.permanent = True

        if login.current_user.is_authenticated():
            if 'target' in request.args:
                return redirect(request.args['target'])
            return redirect(url_for('.index'))
        link = u'<p>Не имеете аккаунта? <a id="a_reg" href="' + url_for('.register_view') + u'">Нажмите для регистрации.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return self.render("login.html")

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()
            profile = Profile()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.password = generate_password_hash(form.password.data)
            profile.user = user

            db.session.add(user)
            db.session.add(profile)
            db.session.commit()

            login.login_user(user)
            return redirect(url_for('.index'))
        link = u'<p>Уже имеете аккаунт? <a id="a_entry" href="' + url_for('.login_view') + u'">Нажмите для входа.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return self.render("login.html")

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))