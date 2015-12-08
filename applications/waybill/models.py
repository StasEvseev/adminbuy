# coding: utf-8

from flask import url_for
from sqlalchemy_utils import ChoiceType
from db import db

__author__ = 'StasEvseev'


FROM_MAIL = 1
FROM_ACCEPTANCE = 2
FROM_CUSTOM = 3
TYPES = {
    FROM_MAIL: u"Письмо",
    FROM_ACCEPTANCE: u"Приемка",
    FROM_CUSTOM: u"Новая"
}

RETAIL = 1
GROSS = 2
TYPE = {RETAIL: u"Розничная", GROSS: u"Оптовая"}

DRAFT, IN_PROG, IN_DELIVERY, FINISH = 1, 2, 3, 4

StatusType = {
    DRAFT: u"Черновик",
    IN_PROG: u"Оформление",
    IN_DELIVERY: u"Доставка",
    FINISH: u"Доставлено",
}

POINTSALE, RECEIVER = 1, 2
RecType = {
    POINTSALE: "Pointsale",
    RECEIVER: "Receiver"
}


class WayBill(db.Model):
    """
    накладная.
    """
    id = db.Column(db.Integer, primary_key=True)
    # Номер
    number = db.Column(db.String(250))
    # Дата накладной
    date = db.Column(db.Date)

    # Торговая точка - откуда пересылают товар
    pointsale_from_id = db.Column(db.Integer, db.ForeignKey('point_sale.id'))
    pointsale_from = db.relationship(
        'PointSale', foreign_keys='WayBill.pointsale_from_id',
        backref=db.backref('from_waybills', lazy='dynamic'))

    receiver_id = db.Column(db.Integer, db.ForeignKey('receiver.id'))
    receiver = db.relationship(
        'Receiver', backref=db.backref('waybills', lazy='dynamic'))

    pointsale_id = db.Column(db.Integer, db.ForeignKey('point_sale.id'))
    pointsale = db.relationship(
        'PointSale', foreign_keys='WayBill.pointsale_id',
        backref=db.backref('waybills', lazy='dynamic'))

    type = db.Column(ChoiceType(TYPE), default=RETAIL)

    typeRec = db.Column(ChoiceType(RecType), default=POINTSALE)
    # Основание
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    invoice = db.relationship(
        'Invoice', backref=db.backref('waybills', lazy='dynamic'))

    status = db.Column(ChoiceType(StatusType), default=DRAFT)

    # Файл накладной
    file = db.Column(db.String)

    def from_type(self):
        if self.invoice_id is None:
            return FROM_CUSTOM
        elif self.pointsale_from_id is None:
            return FROM_MAIL
        else:
            return FROM_ACCEPTANCE

    @property
    def rec(self):
        if self.receiver:
            return self.receiver.fullname
        elif self.pointsale:
            return self.pointsale.name
        else:
            return "Накладная не имеет получателя"

    @property
    def filepath(self):
        return url_for('static', filename='files/' + self.file.split("/")[-1])

    def __repr__(self):
        return '<WayBill %r>' % self.number


class WayBillItems(db.Model):
    """
    Позиция в накладной.
    """
    id = db.Column(db.Integer, primary_key=True)

    # накладная
    waybill_id = db.Column(db.Integer, db.ForeignKey('way_bill.id'))
    waybill = db.relationship(
        'WayBill', backref=db.backref('items', lazy='dynamic'))

    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    good = db.relationship(
        'Good', backref=db.backref('waybillitems', lazy='dynamic'))

    count = db.Column(db.Integer)

    def __repr__(self):
        return '<WayBillItems %r>' % self.good.full_name or ''
