# coding: utf-8

from adminbuy.db import db

__author__ = 'StasEvseev'


class Revision(db.Model):
    """
    Моделька ревизии
    """
    __tablename__ = 'revision'
    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.Date)

    pointsale_id = db.Column(db.Integer, db.ForeignKey('point_sale.id'))
    pointsale = db.relationship(
        'applications.point_sale.models.PointSale',
        backref=db.backref('revisions', lazy='dynamic'))

    seller_id = db.Column(db.Integer, db.ForeignKey("seller.id"))
    seller = db.relationship(
        'applications.seller.model.Seller',
        backref=db.backref('revisions', lazy='dynamic'))


class RevisionItem(db.Model):
    __tablename__ = 'revision_item'
    id = db.Column(db.Integer, primary_key=True)

    revision_id = db.Column(db.Integer, db.ForeignKey('revision.id'))
    revision = db.relationship(
        Revision,
        backref=db.backref('items', lazy=True))

    # Товар в системе
    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    good = db.relationship(
        'applications.good.model.Good',
        backref=db.backref('revisions', uselist=False))

    count_before = db.Column(db.Integer)
    count_after = db.Column(db.Integer)
