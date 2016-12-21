# coding: utf-8

from sqlalchemy_utils import ChoiceType

from adminbuy.db import db


__author__ = 'StasEvseev'


RETAIL = 1
GROSS = 2
TYPE = {RETAIL: u"Розничная", GROSS: u"Оптовая"}

DRAFT, IN_PROG, IN_DELIVERY, IN_POINT, IN_CALC, FINISH = 1, 2, 3, 4, 5, 6

StatusType = {
    DRAFT: u"Черновик",
    IN_PROG: u"Оформление",
    IN_DELIVERY: u"Доставка",
    IN_POINT: u"На точке",
    IN_CALC: u"В обработке",
    FINISH: u"Завершено",
}

POINTSALE, RECEIVER = 1, 2
RecType = {
    POINTSALE: "Pointsale",
    RECEIVER: "Receiver"
}


class WayBillReturn(db.Model):
    """
    накладная.
    """
    __tablename__ = 'way_bill_return'

    id = db.Column(db.Integer, primary_key=True)
    # Номер
    number = db.Column(db.String(250))
    # Дата накладной
    date = db.Column(db.Date)
    date_to = db.Column(db.Date)

    receiver_id = db.Column(db.Integer, db.ForeignKey('receiver.id'))
    receiver = db.relationship(
        'applications.receiver.model.Receiver',
        backref=db.backref('waybillreturns', lazy='dynamic'))

    pointsale_id = db.Column(db.Integer, db.ForeignKey('point_sale.id'))
    pointsale = db.relationship(
        'applications.point_sale.models.PointSale',
        backref=db.backref('waybillreturns', lazy='dynamic'))

    type = db.Column(ChoiceType(TYPE), default=RETAIL)

    typeRec = db.Column(ChoiceType(RecType), default=POINTSALE)
    # Основание
    returninst_id = db.Column(db.Integer, db.ForeignKey('return.id'))
    returninst = db.relationship(
        'applications.return_app.model.Return',
        backref=db.backref('waybillreturns', lazy='dynamic'))

    status = db.Column(ChoiceType(StatusType), default=DRAFT)

    @property
    def rec(self):
        if self.receiver:
            return self.receiver.fullname
        elif self.pointsale:
            return self.pointsale.name
        else:
            return "Накладная не имеет получателя"

    def __repr__(self):
        return '<WayBillReturn %r>' % self.number


class WayBillReturnItems(db.Model):
    """
    Позиция в накладной.
    """
    __tablename__ = 'way_bill_return_items'

    id = db.Column(db.Integer, primary_key=True)

    # накладная
    waybill_id = db.Column(db.Integer, db.ForeignKey('way_bill_return.id'))
    waybill = db.relationship(
        WayBillReturn,
        backref=db.backref('items', lazy='dynamic'))

    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    good = db.relationship(
        'applications.good.model.Good',
        backref=db.backref('waybillreturnitems', lazy='dynamic'))

    count_plan = db.Column(db.Integer)

    count = db.Column(db.Integer)

    def __repr__(self):
        return '<WayBillReturnItems %r>' % self.good.full_name or ''
