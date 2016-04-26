# coding: utf-8

from tasks.instance import celery
from flask.ext.mail import Mail

from app import app


mail = Mail(app)


class SingletoneSMTPHandler(object):
    object = None

    @classmethod
    def obj(cls):
        from config import ADMINS, admin_imap, admin_pass
        import logging
        from logging.handlers import SMTPHandler
        if not cls.object:
            smtp = SMTPHandler(
                'smtp.gmail.com',
                'server-error@example.com',
                ADMINS, 'BuyApi Failed',
                credentials=(admin_imap, admin_pass),
                secure=())
            smtp.setFormatter(logging.Formatter('''
                Message type:       %(levelname)s
                Time:               %(asctime)s
                Message:
                %(message)s
            '''))
            cls.object = smtp
        else:
            smtp = cls.object
        return smtp


@celery.task
def send_async_email(msg):
    """
    Селери задача, отправки писем из очереди.
    """
    mail.send(msg)


@celery.task(name="send_ERROR")
def send_error(record):
    """
    Селери задача по отправке ошибок из очереди.
    """
    SingletoneSMTPHandler.obj().emit(record)


# def send_mail_async(title, message):
#     # from tasks import send_async_email
#     from config import ADMINS
#     msg = Message(title, recipients=ADMINS)
#     msg.body = message
#     send_async_email.apply_async(args=[msg])
