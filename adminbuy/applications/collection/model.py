# coding: utf-8

from datetime import date

from adminbuy.db import db


__author__ = 'StasEvseev'


class Collect(db.Model):
    __tablename__ = 'collect'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today)

    location_id = db.Column(db.Integer, db.ForeignKey('point_sale.id'))
    location = db.relationship(
        'applications.point_sale.models.PointSale',
        backref=db.backref('collects', lazy='dynamic'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'applications.security.models.User',
        backref=db.backref('collects', lazy='dynamic'))

    sum = db.Column(db.DECIMAL)

    @property
    def name(self):
        return u"Сбор %s с точки %s" % (self.date, self.location.name)
