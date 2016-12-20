# coding: utf-8

from adminbuy.db import db


class Profile(db.Model):
    """
    Единица товара
    """
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(
        'applications.security.models.User',
        backref=db.backref('profiles', lazy='dynamic'))

    rate_retail = db.Column(db.DECIMAL, default=1.6)
    rate_gross = db.Column(db.DECIMAL, default=1.4)
