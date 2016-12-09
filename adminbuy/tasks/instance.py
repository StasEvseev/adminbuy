# coding: utf-8

from datetime import timedelta

from celery import Celery

from adminbuy.app import app


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
            'task': 'tasks.regular.run_every_minute',
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
