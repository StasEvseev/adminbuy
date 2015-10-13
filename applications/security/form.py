#coding: utf-8

__author__ = 'StasEvseev'

# from wtforms import form, fields, validators
# from werkzeug.security import check_password_hash
#
# from db import db
# from applications.security.model import User
#
#
# class LoginForm(form.Form):
#     login = fields.TextField(validators=[validators.required()])
#     password = fields.PasswordField(validators=[validators.required()])
#
#     def __init__(self, *args, **kwargs):
#         super(LoginForm, self).__init__(*args, **kwargs)
#
#         self.login.type = "text"
#         self.login.label = u"Имя"
#         self.password.type = "password"
#         self.password.label = u"Пароль"
#
#     def validate_login(self, field):
#         """
#         Проверяем логин
#         """
#         user = self.get_user()
#
#         if user is None:
#             raise validators.ValidationError('Invalid user')
#
#         # we're comparing the plaintext pw with the the hash from the db
#         if not check_password_hash(user.password, self.password.data):
#         # to compare plain text passwords use
#         # if user.password != self.password.data:
#             raise validators.ValidationError('Invalid password')
#
#     def get_user(self):
#         """
#         Получаем пользователя
#         """
#         return db.session.query(User).filter_by(login=self.login.data).first()
#
#
# class RegistrationForm(form.Form):
#     login = fields.TextField(validators=[validators.required()])
#     email = fields.TextField()
#     password = fields.PasswordField(validators=[validators.required()])
#
#     def __init__(self, *args, **kwargs):
#         super(RegistrationForm, self).__init__(*args, **kwargs)
#
#         self.login.type = "text"
#         self.login.label = u"Имя"
#         self.email.type = "text"
#         self.email.label = u"Адрес"
#         self.password.type = "password"
#         self.password.label = u"Пароль"
#
#     def validate_login(self, field):
#         if db.session.query(User).filter_by(login=self.login.data).count() > 0:
#             raise validators.ValidationError('Duplicate username')