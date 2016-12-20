# coding: utf-8

from adminbuy.db import db

__author__ = 'StasEvseev'


# TODO: deprecated
class RetailInvoiceItem(db.Model):
    """
    Позиция в розничной накладной.
    """
    id = db.Column(db.Integer, primary_key=True)

    # Розничная накладная
    retailinvoice_id = db.Column(db.Integer, db.ForeignKey('retail_invoice.id'))
    retailinvoice = db.relationship(
        'retail.models.RetailInvoice', backref=db.backref('retailinvoiceitems',
                                            lazy='dynamic'))

    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    good = db.relationship(
        'applications.good.model.Good',
        backref=db.backref('retailinvoiceitems', lazy='dynamic'))

    def __repr__(self):
        return '<RetailInvoiceItem %r>' % self.good.full_name or ''
