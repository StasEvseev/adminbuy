# coding: utf-8

from flask.ext.script import Command, Option


class ChangePassword(Command):
    option_list = (
        Option('--login', '-l', dest='login', required=True),
        Option('--password', '-p', dest='password', required=True),
    )

    def run(self, login, password):
        from app import app
        app.change_password(login, password)
