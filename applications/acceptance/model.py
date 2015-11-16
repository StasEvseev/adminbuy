# coding: utf-8

from sqlalchemy_utils import ChoiceType
from db import db

__author__ = 'StasEvseev'


MAIL, NEW = 1, 2
RecType = {
    MAIL: u"Регулярная по почте",
    NEW: u"Новая"
}

DRAFT, IN_PROG, VALIDATED = 1, 2, 3

StatusType = {
    DRAFT: u"Черновик",
    IN_PROG: u"В процессе",
    VALIDATED: u"Подтверждено",
}


class Acceptance(db.Model):
    """
    Приемка товара
    """
    id = db.Column(db.Integer, primary_key=True)

    pointsale_id = db.Column(db.Integer, db.ForeignKey('point_sale.id'))
    pointsale = db.relationship(
        'PointSale', backref=db.backref('acceptances', lazy=True))
    # Накладная основание
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), unique=True)
    invoice = db.relationship(
        'Invoice', backref=db.backref('acceptance', uselist=False))
    waybill_id = db.Column(
        db.Integer, db.ForeignKey('way_bill.id'), unique=True)
    waybill = db.relationship('WayBill', backref=db.backref(
        'acceptance', uselist=False))

    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))
    provider = db.relationship(
        'Provider', backref=db.backref('acceptances', lazy='dynamic'))

    # Дата приема товара
    date = db.Column(db.Date)

    type = db.Column(ChoiceType(RecType), default=MAIL)
    status = db.Column(ChoiceType(StatusType), default=DRAFT)

    def __repr__(self):
        return '<Acceptance %r>' % self.id

    @property
    def receiver(self):
        if self.type == MAIL:
            return self.invoice.provider.name
        elif self.type == NEW:
            return self.provider.name
        return u"Неизвестный"


# class LinkAcceptanceInvoice(db.Model):
#
#     id = db.Column(db.INTEGER, primary_key=True)
#
#     acceptance_id = db.Column(db.INTEGER, db.ForeignKey('acceptance.id'),
#                               doc=u"Поле для связи с Acceptance")
#     invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
#     invoice = db.relationship(
#         'Invoice', backref=db.backref('acceptance', uselist=False))


class AcceptanceItems(db.Model):
    """
    Позиция в накладной.
    """
    id = db.Column(db.Integer, primary_key=True)

    # накладная
    acceptance_id = db.Column(db.Integer, db.ForeignKey('acceptance.id'))
    acceptance = db.relationship(
        'Acceptance', backref=db.backref('items', lazy='dynamic'))

    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    good = db.relationship(
        'Good', backref=db.backref('acceptanceitems', lazy='dynamic'))

    count = db.Column(db.Integer)
    fact_count = db.Column(db.Integer)

    def __repr__(self):
        return '<AcceptanceItems %r>' % self.good.full_name or ''
