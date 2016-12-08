# coding: utf-8

from flask.ext.script import Command


class SuperUserCommand(Command):
    """

    Команда создания суперпользователя.

    """
    def run(self):
        from app import app
        app.create_superuser()
