# coding: utf-8

from adminbuy.db import db


__author__ = 'StasEvseev'


class Order(db.Model):
    """
    Модель заказа
    """
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    # Заказ с
    date_start = db.Column(db.Date)
    # Заказ по
    date_end = db.Column(db.Date)
    # Поставщик
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))
    provider = db.relationship(
        'applications.provider_app.models.Provider',
        backref=db.backref('orders', lazy='dynamic'))

    def __repr__(self):
        return '<Order from %r>' % self.provider.name


class OrderItem(db.Model):
    """
    Позиция в заказе.
    """
    __tablename__ = 'order_item'

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(250))
    number_local = db.Column(db.String(250))
    number_global = db.Column(db.String(250))

    # Название издания
    name = db.Column(db.String(250))
    # Ориент. дата выхода
    date = db.Column(db.Date)
    # Рем%
    remission = db.Column(db.DECIMAL)
    # НДС%
    NDS = db.Column(db.DECIMAL)
    # Заказ клиента
    count = db.Column(db.Integer)

    # Пред цена
    price_prev = db.Column(db.DECIMAL)
    # Пост цена
    price_post = db.Column(db.DECIMAL)

    # Товар в системе
    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    good = db.relationship(
        'applications.good.model.Good',
        backref=db.backref('orderitem', lazy='dynamic'))

    # Заказ
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship(
        Order,
        backref=db.backref('items', lazy='dynamic'))

    def __repr__(self):
        return '<OrderItem %r>' % self.name
