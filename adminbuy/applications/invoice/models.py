# coding: utf-8

from adminbuy.db import db


__author__ = 'StasEvseev'


x = 1


class Invoice(db.Model):
    """
    Приходная накладная.
    """
    __tablename__ = 'invoice'

    id = db.Column(db.Integer, primary_key=True)
    # Номер
    number = db.Column(db.String(250))
    # Дата накладной
    date = db.Column(db.Date)
    # Поставщик
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))
    provider = db.relationship(
        'applications.provider_app.models.Provider',
        backref=db.backref('invoices', lazy='dynamic'))

    # Сумма без НДС, руб.
    sum_without_NDS = db.Column(db.DECIMAL)
    # Сумма с учетом НДС, руб.
    sum_with_NDS = db.Column(db.DECIMAL)
    # Сумма НДС, руб.
    sum_NDS = db.Column(db.DECIMAL)

    # Вес товара
    weight = db.Column(db.DECIMAL)
    # Отпустил
    responsible = db.Column(db.String(250))

    def __unicode__(self):
        return u'Накладная %s от %s' % (self.number, self.date)

    @property
    def fullname(self):
        return unicode(self)

    @property
    def is_acceptance(self):
        from adminbuy.applications.acceptance.service import AcceptanceService
        acc = AcceptanceService.get_by_invoice_id(self.id)

        return True if acc else False

    @property
    def acceptance_id(self):
        from adminbuy.applications.acceptance.service import AcceptanceService
        acc = AcceptanceService.get_by_invoice_id(self.id)
        return acc.id


class InvoiceItem(db.Model):
    """
    Элемент приходной накладной
    """
    __tablename__ = 'invoice_item'

    id = db.Column(db.Integer, primary_key=True)

    # Полное наименование издания
    full_name = db.Column(db.String(250))
    # Название издания
    name = db.Column(db.String(250))
    # Номер издания
    number_local = db.Column(db.String(250))

    number_global = db.Column(db.String(250))

    # Заказ
    count_order = db.Column(db.Integer)
    # Дозак
    count_postorder = db.Column(db.Integer)
    # Количество
    count = db.Column(db.Integer)

    # "Цена Без НДС, руб."
    price_without_NDS = db.Column(db.DECIMAL)
    # "Цена с НДС, руб."
    price_with_NDS = db.Column(db.DECIMAL)
    # Сумма без НДС, руб.
    sum_without_NDS = db.Column(db.DECIMAL)
    # Сумма НДС, руб.
    sum_NDS = db.Column(db.DECIMAL)
    # Ставка НДС
    rate_NDS = db.Column(db.DECIMAL)
    # Сумма с учетом НДС, руб.
    sum_with_NDS = db.Column(db.DECIMAL)

    # Тематика изд.
    thematic = db.Column(db.String(250))
    # Целых пачек
    count_whole_pack = db.Column(db.Integer)
    # Россыпь (экз.)
    placer = db.Column(db.Integer)

    # Накладная
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    invoice = db.relationship(
        Invoice,
        backref=db.backref('items', lazy='dynamic'))

    fact_count = db.Column(db.Integer)

    # Товар в системе
    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    good = db.relationship(
        'applications.good.model.Good',
        backref=db.backref('invoiceitem', lazy='dynamic'))

    # Розничная цена
    price_retail = db.Column(db.DECIMAL)
    # Оптовая цена
    price_gross = db.Column(db.DECIMAL)

    def __repr__(self):
        return '<InvoiceItem %r>' % self.name
