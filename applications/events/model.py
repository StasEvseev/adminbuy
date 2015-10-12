# coding: utf-8
from sqlalchemy_utils import ChoiceType
from db import db

__author__ = 'user'


MAIL = 1
INVOICE = 2
TYPE = {MAIL: u"Приход почты", INVOICE: u"Формирование накладной"}


class Event(db.Model):
    """
    Событие
    """
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(ChoiceType(TYPE), default=MAIL)
    datetime = db.Column(db.DateTime())
    data = db.Column(db.TEXT)