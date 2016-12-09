# coding: utf-8

from sqlalchemy_utils import ChoiceType

from adminbuy.db import db

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


linkacceptanceinvoice = db.Table('linkacceptanceinvoice',
    db.Column('acceptance_id', db.Integer, db.ForeignKey('acceptance.id')),
    db.Column('invoice_id', db.Integer, db.ForeignKey('invoice.id'))
)


class Acceptance(db.Model):
    """
    Приемка товара
    """
    id = db.Column(db.Integer, primary_key=True)

    pointsale_id = db.Column(db.Integer, db.ForeignKey('point_sale.id'))
    pointsale = db.relationship(
        'PointSale', backref=db.backref('acceptances', lazy=True))

    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))
    provider = db.relationship(
        'Provider', backref=db.backref('acceptances', lazy='dynamic'))

    # Дата приема товара
    date = db.Column(db.Date)

    type = db.Column(ChoiceType(RecType), default=MAIL)
    status = db.Column(ChoiceType(StatusType), default=DRAFT)

    invoices = db.relationship('Invoice', secondary=linkacceptanceinvoice,
                               backref=db.backref('acceptances', lazy='dynamic'))

    def __repr__(self):
        return '<Acceptance %r>' % self.id

    @property
    def display_invoices(self):
        disp_inv = ""
        if self.type == MAIL:
            invoices = self.invoices
            invoices_numbers = [invoice.number for invoice in invoices]
            disp_inv = u", ".join(invoices_numbers)
            if len(invoices) > 2:
                disp_inv += u", ..."
        return disp_inv

    @property
    def display(self):
        if self.type == MAIL:
            disp_inv = self.display_invoices
            return u"Приемка накладных(%s)" % disp_inv
        elif self.type == NEW:
            return u"Приемка накладной от %s" % self.provider.name
        return u"Неверный тип"

    @property
    def receiver(self):
        if self.type == MAIL:
            return self.invoice.provider.name
        elif self.type == NEW:
            return self.provider.name
        return u"Неизвестный"


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

    # TO FRONTEND
    @property
    def fact_count_front(self):
        return self.fact_count or self.count
