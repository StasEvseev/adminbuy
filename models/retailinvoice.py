# coding: utf-8

from db import db

__author__ = 'StasEvseev'


# TODO: deprecated
class RetailInvoice(db.Model):
    """
    Розничная накладная.
    """
    id = db.Column(db.Integer, primary_key=True)
    # Номер
    number = db.Column(db.String(250))
    # Дата накладной
    date = db.Column(db.Date)

    # Основание
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    invoice = db.relationship(
        'Invoice', backref=db.backref('retailinvoices', lazy='dynamic'))

    # Файл накладной
    file = db.Column(db.String)

    def __repr__(self):
        return '<RetailInvoice %r>' % self.number
