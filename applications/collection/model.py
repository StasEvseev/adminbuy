#coding: utf-8

from datetime import date
from db import db


class Collect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today)
    location_id = db.Column(db.Integer, db.ForeignKey('point_sale.id'))
    location = db.relationship('PointSale', backref=db.backref('collects', lazy='dynamic'))
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'))
    seller = db.relationship('Seller', backref=db.backref('collects', lazy='dynamic'))
    sum = db.Column(db.DECIMAL)

    @property
    def name(self):
        return u"Сбор %s с точки %s" % (self.date, self.location.name)