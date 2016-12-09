# coding:utf-8

from flask import json

from adminbuy.db import db

from adminbuy.applications.return_app.model import Return


class Mail(db.Model):
    __tablename__ = 'mails'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    date = db.Column(db.DateTime(timezone=True))
    from_ = db.Column(db.String)
    to = db.Column(db.String)
    text = db.Column(db.String)
    files = db.Column(db.String)
    is_handling = db.Column(db.BOOLEAN)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))
    provider = db.relationship(
        'Provider', backref=db.backref('mails', lazy='dynamic'))
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    invoice = db.relationship(
        'Invoice', backref=db.backref('mails', lazy='dynamic'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship(
        'Order', backref=db.backref('mails_from_order', lazy='dynamic'))
    return_id = db.Column(db.Integer, db.ForeignKey('return.id'))
    return_item = db.relationship(
        Return, backref=db.backref('mails_from_return', lazy='dynamic'))

    def __init__(self, title, date, from_, to, text, files=None,
                 is_handling=False):
        self.title = title
        self.date = date
        self.from_ = from_
        self.to = to
        self.text = text
        self.files = json.dumps(files)
        self.is_handling = is_handling

    def __repr__(self):
        return "<Mail ('%s', '%s')>" % (self.title, self.date)

    def get_file_to_index(self, index):
        return json.loads(self.files)[index]

    @property
    def files_(self):
        return json.loads(self.files)

    @property
    def provider_name(self):
        prov = None
        if self.provider:
            prov = self.provider
        elif self.invoice:
            prov = self.invoice.provider
        elif self.order:
            prov = self.order.provider
        elif self.return_item:
            prov = self.return_item.provider

        return prov.name if prov else u""
