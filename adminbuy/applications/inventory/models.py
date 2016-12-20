# coding:utf-8

import datetime as dtmodule

from sqlalchemy_utils.types.choice import ChoiceType

from adminbuy.db import db


DRAFT, IN_PROG, VALIDATED = 1, 2, 3

StatusType = {
    DRAFT: u"Черновик",
    IN_PROG: u"В процессе",
    VALIDATED: u"Подтверждено",
}


class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    # Номер
    number = db.Column(db.String(250))
    # Дата ревизии
    datetimenew = db.Column(
        db.DateTime(timezone=True), default=dtmodule.datetime.now)
    location_id = db.Column(db.Integer, db.ForeignKey('point_sale.id'))
    location = db.relationship(
        'applications.point_sale.models.PointSale',
        backref=db.backref('inventors'))

    of = db.Column(db.SmallInteger)

    status = db.Column(ChoiceType(StatusType), default=DRAFT)

    def __unicode__(self):
        return u"Инвентаризация №(%s)%s в %s" % (
            self.number, u" от %s" % self.datetimenew if self.datetimenew
            else u"", self.location)


class InventoryItems(db.Model):
    __tablename__ = 'inventory_items'

    id = db.Column(db.Integer, primary_key=True)

    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'))
    inventory = db.relationship(
        Inventory, backref=db.backref('items'))

    # Товар в системе
    good_id = db.Column(db.Integer, db.ForeignKey('good.id'))
    good = db.relationship(
        'applications.good.model.Good',
        backref=db.backref('inventarisations'))
    count_before = db.Column(db.Integer)
    count_after = db.Column(db.Integer)
