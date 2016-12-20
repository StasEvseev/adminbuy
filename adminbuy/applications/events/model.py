# coding: utf-8

from sqlalchemy_utils import ChoiceType

from adminbuy.db import db


class Event(db.Model):
    """
    Событие
    """
    # __tablename__ = 'event'

    MAIL = 1
    INVOICE = 2
    INVOICE_PACK = 3
    TYPE = {
        MAIL: u"Приемка почты",
        INVOICE: u"Формирование накладной",
        INVOICE_PACK: u"Формирование пачки накладных"
    }

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(ChoiceType(TYPE), default=MAIL)
    datetime = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'security.models.User', backref=db.backref('events', lazy='dynamic'))
    data = db.Column(db.TEXT)
