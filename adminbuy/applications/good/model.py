# coding: utf-8

from adminbuy.db import db


__author__ = 'StasEvseev'


class Good(db.Model):
    """
    Товар
    """
    __tablename__ = 'good'

    id = db.Column(db.Integer, primary_key=True)
    # штрих код
    barcode = db.Column(db.BigInteger)

    # Полное наименование
    full_name = db.Column(db.String(250))
    # Продукция
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'))
    commodity = db.relationship(
        'applications.commodity.models.Commodity',
        backref=db.backref('goods', lazy='dynamic'))

    number_local = db.Column(db.String(250))
    number_global = db.Column(db.String(250))
    # Цена на продукцию
    price_id = db.Column(db.Integer, db.ForeignKey('price.id'))
    price = db.relationship(
        'applications.price.model.Price',
        backref=db.backref('goods', lazy='dynamic'))

    @property
    def full_name_with_price(self):
        return (
            self.full_name + u" (" + (u"розн. - " + unicode(
                float(self.price.price_retail)) + u", "
                                      if self.price and self.price.price_retail
                                      else u"") + (
                u"опт. - " + unicode(float(self.price.price_gross))
                if self.price and self.price.price_gross else u"") + u")")
