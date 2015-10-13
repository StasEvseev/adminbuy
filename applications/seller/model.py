#coding: utf-8

__author__ = 'StasEvseev'


#Продавец
from db import db


class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    fname = db.Column(db.String(250))
    lname = db.Column(db.String(250))
    pname = db.Column(db.String(250))

    address = db.Column(db.String(250))

    passport = db.Column(db.String(250))

    @property
    def fullname(self):
        return " ".join([self.lname or "", self.fname or "", self.pname or ""])