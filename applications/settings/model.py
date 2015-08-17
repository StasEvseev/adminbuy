#coding: utf-8

from db import db


class Profile(db.Model):
    """
    Единица товара
    """
    id = db.Column(db.Integer, primary_key=True)

    # user_id = db.Column()

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('profiles', lazy='dynamic'))

    rate_retail = db.Column(db.DECIMAL, default=1.6)
    rate_gross = db.Column(db.DECIMAL, default=1.4)

    #Розничная цена
    # price_retail = db.Column(db.DECIMAL)
    #Оптовая цена
    # price_gross = db.Column(db.DECIMAL)

    # def __repr__(self):
    #     return '<Price to %r from %s (%s, %s)>' % (self.commodity.name, self.date_from, self.price_retail or "", self.price_gross or "")