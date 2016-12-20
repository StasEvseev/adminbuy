# coding: utf-8

from adminbuy.db import db

__author__ = 'StasEvseev'


class SyncSession(db.Model):
    __tablename__ = 'sync_session'
    id = db.Column(db.Integer, primary_key=True)
    # Дата
    datetime = db.Column(db.DateTime)
    deviceId = db.Column(db.String)


class WorkDay(db.Model):
    """
    Рабочий день на торговой точке.
    """
    __tablename__ = 'work_day'
    id = db.Column(db.Integer, primary_key=True)
    datetime_start = db.Column(db.DateTime)
    datetime_end = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'applications.security.models.User',
        backref=db.backref('workdays', lazy='dynamic'))

    username = db.Column(db.String)

    sync_start_id = db.Column(db.Integer, db.ForeignKey('sync_session.id'))
    sync_start = db.relationship(
        SyncSession,
        backref=db.backref('workday_start', lazy='dynamic'),
        foreign_keys='WorkDay.sync_start_id')

    sync_end_id = db.Column(db.Integer, db.ForeignKey('sync_session.id'))
    sync_end = db.relationship(
        SyncSession, backref=db.backref('workday_end', lazy='dynamic'),
        foreign_keys='WorkDay.sync_end_id')


class SyncItemSession(db.Model):
    __tablename__ = 'sync_item_session'
    id = db.Column(db.Integer, primary_key=True)

    sync_id = db.Column(db.Integer, db.ForeignKey('sync_session.id'))
    sync = db.relationship(
        SyncSession, backref=db.backref('items', lazy='dynamic'))

    workday_id = db.Column(db.Integer, db.ForeignKey('work_day.id'))
    workday = db.relationship(
        WorkDay, backref=db.backref('workdayitems', lazy='dynamic'))

    barcode = db.Column(db.String)
    datetime = db.Column(db.DateTime)
    operation = db.Column(db.Integer)
    count = db.Column(db.Integer)


class Sync(db.Model):
    __tablename__ = 'sync'

    id = db.Column(db.Integer, primary_key=True)
    # Дата начала
    date_start = db.Column(db.DateTime)
    # Дата накладной
    date_end = db.Column(db.DateTime)
    # Статус енам
    status = db.Column(db.Integer)

    @property
    def status_string(self):
        return ENUM_STATUS[self.status]

IN_PROGRESS = 1
COMPLETE = 2
CANCEL = 3
TIMEOUT = 4
NO_CONN = 5
IOERROR = 6
BATCH_ERROR = 7
AUTH_ERROR = 8

ENUM_STATUS = {
    IN_PROGRESS: u"В процессе",
    COMPLETE: u"Закончен",
    CANCEL: u"Отменен",
    TIMEOUT: u"Долгий отклик",
    NO_CONN: u"Нет соединения",
    IOERROR: u"Проблемы с вводом/выводом",
    BATCH_ERROR: u"Ошибка массового сохранения",
    AUTH_ERROR: u"Проблемы авторизации в приложении",
}
