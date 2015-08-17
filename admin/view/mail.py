#coding: utf-8
from flask.ext import login
from angular.view import ProjectAngularView


class MailView(ProjectAngularView):

    def index_view(self):
        return self.render('mail/mail.html', token=login.current_user.generate_auth_token())