# coding: utf-8

from adminbuy.db import db

__author__ = 'StasEvseev'


class Price(db.Model):
    """
    Единица товара
    """
    __tablename__ = 'price'

    id = db.Column(db.Integer, primary_key=True)

    # Розничная цена
    price_retail = db.Column(db.DECIMAL)
    # Оптовая цена
    price_gross = db.Column(db.DECIMAL)

    def __repr__(self):
        return '<Price to %r from %s (%s, %s)>' % (
            self.commodity.name, self.date_from, self.price_retail or "",
            self.price_gross or "")


class PriceParish(db.Model):
    """
    Цена прихода
    """
    __tablename__ = 'price_parish'

    id = db.Column(db.Integer, primary_key=True)
    commodity_id = db.Column(
        db.Integer, db.ForeignKey('commodity.id'), nullable=False)
    commodity = db.relationship(
        'applications.commodity.models.Commodity',
        backref=db.backref('priceparish'))

    number_local_from = db.Column(db.String(250))
    number_global_from = db.Column(db.String(250))

    date_from = db.Column(db.Date)

    NDS = db.Column(db.DECIMAL)
    # Пред цена
    price_prev = db.Column(db.DECIMAL)
    # Пост цена
    price_post = db.Column(db.DECIMAL, nullable=False)

    price_id = db.Column(db.Integer, db.ForeignKey('price.id'), nullable=False)
    price = db.relationship(
        Price,
        backref=db.backref('priceparish'))
    # Накладная основание
    invoice_id = db.Column(
        db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    invoice = db.relationship(
        'applications.invoice.models.Invoice',
        backref=db.backref('priceparish'))
