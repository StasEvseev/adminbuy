# coding: utf-8

import logging
from logging.handlers import RotatingFileHandler
from kombu.exceptions import EncodeError
import traceback

from config import admin_imap, admin_pass

MAX_BYTES = 1048576
BACKUP_COUNT = 50
LOG_FILE_NAME_ERROR = "logs/error.log"
LOG_FILE_NAME_WARNING = "logs/warning.log"
LOG_FILE_NAME_DEBUG = "logs/debug.log"


class MyHandler(logging.Handler):
    """
    Обработчик, исключений. Ставящий задания в очередь по отправке ошибок на
    почту.
    """

    def __init__(self, *args, **kwargs):
        super(MyHandler, self).__init__(*args, **kwargs)

    def emit(self, record):
        from tasks.mailmodule import send_error
        try:
            send_error.apply_async([record])
        except EncodeError as exc:
            # при ошибке сериализации записи, оповестить
            # ошибку взбросить выше
            tracebackold = traceback.format_exc()
            t, e, tr = record.exc_info
            try:
                raise e, None, tr
            except Exception:
                error(u"Произошла ошибка при конвертации: " +
                      unicode(tracebackold) + "\n>>>>>\n")
                raise


def init_logging(application):
    if admin_imap and admin_pass:
        my_h = MyHandler()
        my_h.setLevel(logging.ERROR)
        application.logger.addHandler(my_h)
    rotate_handler1 = RotatingFileHandler(
        LOG_FILE_NAME_ERROR, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
    rotate_handler1.setLevel(logging.ERROR)
    rotate_handler1.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
    ))
    application.logger.addHandler(rotate_handler1)

    rotate_handler2 = RotatingFileHandler(
        LOG_FILE_NAME_WARNING, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
    rotate_handler2.setLevel(logging.WARNING)
    rotate_handler2.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
    ))
    application.logger.addHandler(rotate_handler2)

    rotate_handler3 = RotatingFileHandler(
        LOG_FILE_NAME_DEBUG, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
    rotate_handler3.setLevel(logging.DEBUG)
    rotate_handler3.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
    ))
    application.logger.addHandler(rotate_handler3)
    application.logger.setLevel(logging.DEBUG)


def _mess(message):
    if type(message) == unicode:
        return message.encode("utf-8")
    else:
        return message


def prep_arg(*args):
    res = []
    for ar in args:
        res.append(_mess(ar))
    return tuple(res)


def debug(message, *args):
    from app import app
    app.logger.debug(_mess(message), *prep_arg(*args))


def warning(message, *args):
    from app import app
    app.logger.warn(_mess(message), *prep_arg(*args))


def error(message, *args):
    from app import app
    import traceback
    trace = traceback.format_exc()
    app.logger.error(_mess(message)+"\n"+trace, *prep_arg(*args))
