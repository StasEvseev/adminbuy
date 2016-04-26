# coding: utf-8

from flask.ext.mail import Mail, Message

mail = Mail()


def send_mail_async(title, message):
    from tasks.mailmodule import send_async_email
    from config import ADMINS
    msg = Message(title, recipients=ADMINS)
    msg.body = message
    send_async_email.apply_async(args=[msg])
