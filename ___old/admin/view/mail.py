#coding: utf-8

__author__ = 'StasEvseev'

from flask.ext import login

from old.angular.view import ProjectAngularView


class MailView(ProjectAngularView):

    def index_view(self):
        return self.render('mail/mail.html', token=login.current_user.generate_auth_token())