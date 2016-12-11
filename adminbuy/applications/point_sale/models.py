# coding: utf-8

from adminbuy.db import db


__author__ = 'StasEvseev'


class PointSale(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    address = db.Column(db.String(250))

    is_central = db.Column(db.Boolean, default=False)

    def __unicode__(self):
        if self.is_central:
            text = u"Центральная торговая точка "
        else:
            text = u"Торговая точка "
        return text + self.name


class PointSaleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    pointsale_id = db.Column(db.Integer, db.ForeignKey('point_sale.id'))
    pointsale = db.relationship(
        PointSale, backref=db.backref('items', lazy='dynamic'))

    # Товар в системе
    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    good = db.relationship(
        'Good', backref=db.backref('pointsaleitems', uselist=False))

    count = db.Column(db.Integer)
