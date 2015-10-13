#coding: utf-8

__author__ = 'StasEvseev'

from sqlalchemy_utils import ChoiceType

from db import db

DRAFT, IN_PROG, IN_DEL, FINISH = 1, 2, 3, 4

StatusType = {
    DRAFT: u"Черновик",
    IN_PROG: u"В процессе",
    IN_DEL: u"Отправлено",
    FINISH: u"Подтверждено"
}


class Return(db.Model):
    """
    Модель возврата
    """
    id = db.Column(db.Integer, primary_key=True)
    #Возврат с
    date_start = db.Column(db.Date)
    #Возврат по
    date_end = db.Column(db.Date)
    date = db.Column(db.Date)

    #Поставщик
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))
    provider = db.relationship('Provider',
        backref=db.backref('returns', lazy='dynamic'))

    status = db.Column(ChoiceType(StatusType), default=DRAFT)

    @property
    def name(self):
        return u"Возврат от %s на даты (%s - %s)" % (self.provider.name, self.date_start, self.date_end)

    def __repr__(self):
        return '<Return from %r>' % self.provider.name


class ReturnItem(db.Model):
    """
    Позиция в возврате.
    """
    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(250))
    number_local = db.Column(db.String(250))
    number_global = db.Column(db.String(250))

    #Название издания
    name = db.Column(db.String(250))
    #Ориент. дата выхода
    date = db.Column(db.Date)
    #Дата возврата
    date_to = db.Column(db.Date)

    price_without_NDS = db.Column(db.DECIMAL)
    price_with_NDS = db.Column(db.DECIMAL)

    #Рем%
    remission = db.Column(db.DECIMAL)

    count_delivery = db.Column(db.Integer)

    count_rem = db.Column(db.Integer)

    count = db.Column(db.Integer)

    #Товар в системе
    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    good = db.relationship('Good', backref=db.backref('returnitem', lazy='dynamic'))

    #Заказ
    return_id = db.Column(db.Integer, db.ForeignKey('return.id'))
    return_item = db.relationship('Return',
        backref=db.backref('items', lazy='dynamic'))

    def __repr__(self):
        return '<OrderItem %r>' % self.name