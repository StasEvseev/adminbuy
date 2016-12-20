# coding: utf-8

from adminbuy.db import db


__author__ = 'StasEvseev'


class Receiver(db.Model):
    """
    Получатель.
    """
    __tablename__ = 'receiver'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    # Номер
    fname = db.Column(db.String(250))
    lname = db.Column(db.String(250))
    pname = db.Column(db.String(250))

    address = db.Column(db.String(250))

    passport = db.Column(db.String(250))

    @property
    def fullname(self):
        return " ".join([self.lname or "", self.fname or "", self.pname or ""])
