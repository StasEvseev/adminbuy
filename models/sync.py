#coding: utf-8
from db import db


class SyncSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #Дата
    datetime = db.Column(db.DateTime)
    deviceId = db.Column(db.String)


class SyncItemSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sync_id = db.Column(db.Integer, db.ForeignKey('sync_session.id'))
    sync = db.relationship('SyncSession', backref=db.backref('items', lazy='dynamic'))
    barcode = db.Column(db.String)
    datetime = db.Column(db.DateTime)
    operation = db.Column(db.Integer)
    count = db.Column(db.Integer)


class Sync(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    #Дата начала
    date_start = db.Column(db.DateTime)
    #Дата накладной
    date_end = db.Column(db.DateTime)
    #Статус енам
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