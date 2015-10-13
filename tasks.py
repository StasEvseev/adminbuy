#coding: utf-8

__author__ = 'StasEvseev'

from datetime import timedelta
import redis

from app import app

from celery import Celery
from celery.schedules import crontab


def make_celery(app):
    cel = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    # celery.conf.update(
        # CELERY_IMPORTS=(
            # 'buyapi.tasks',   # we're not including our tasks here as
            # 'app.module_b.tasks',   # our tasks are in other files listed here
        # )
    # )
    cel.conf.update(CELERYBEAT_SCHEDULE={
        # Executes every Monday morning at 7:30 A.M
        'every_minute': {
            'task': 'tasks.run_every_minute',
            'schedule': timedelta(minutes=1),
        },
    }, CELERY_TIMEZONE='Europe/Moscow')

    cel.conf.update(app.config)
    # cel.conf.update(CELERY_TASK_RESULT_EXPIRES=10)
    TaskBase = cel.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    cel.Task = ContextTask
    return cel


celery = make_celery(app)


class A(object):
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
                ADMINS, 'BuyApi Failed', credentials=(admin_imap, admin_pass), secure=())
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
def run_every_minute():
    # from mailmodule import send_mail_async
    # r = redis.StrictRedis(host='localhost', port=6379, db=0)
    print "PUBLISH"
    # r.publish("sms_replies", "%s %s" % ("BLA", "BLA"))
    # send_mail_async(u"1", u"2")


@celery.task(name="send_ERROR")
def send_error(record):
    A.obj().emit(record)


@celery.task
def send_async_email(msg):
    """Background task to send an email with Flask-Mail."""
    from mailmodule import mail
    mail.send(msg)