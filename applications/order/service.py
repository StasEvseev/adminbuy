# coding: utf-8

from db import db
from applications.order.model import Order, OrderItem
from services.core import BaseSQLAlchemyModelService

__author__ = 'StasEvseev'


class OrderService(BaseSQLAlchemyModelService):
    model = Order

    @classmethod
    def create_order(cls, date_start, date_end, provider_id):
        order = Order(date_start=date_start, date_end=date_end,
                      provider_id=provider_id)
        db.session.add(order)
        return order

    @classmethod
    def handle_orderitem(cls, full_name, name, number_local, number_global,
                         date, remission, NDS, price_prev, price_post, order):
        from applications.good.service import GoodService
        from applications.commodity.service import CommodityService
        item = OrderItem()
        item.full_name = full_name,
        item.name = name
        item.number_local = number_local
        item.number_global = number_global
        item.date = date
        item.remission = remission
        item.NDS = float(NDS.replace("%", "").strip())
        item.price_prev = price_prev if price_prev else 0.0
        item.price_post = price_post if price_post else 0.0
        item.order = order

        res, comm = CommodityService.get_or_create_commodity(
            name=name)

        if res is False:
            if not number_local and not number_global:
                comm.numeric = False
            db.session.add(comm)
            db.session.flush()

        res, good = GoodService.get_or_create_commodity_numbers(
            comm.id, number_local, number_global)
        good.commodity = comm
        good.full_name = full_name
        item.good = good
        db.session.add(good)

        db.session.add(item)

    @classmethod
    def set_count_by_id(cls, id, count):
        if count:
            item = OrderItem.query.get(id)
            item.count = count
            db.session.add(item)

    @classmethod
    def get_mail(cls, id):
        mail = None
        order = cls.get_by_id(id)
        if order.mails_from_order.count() > 0:
            mail = order.mails_from_order[0]
        return mail

    @classmethod
    def set_handling(cls, id):
        mail = cls.get_mail(id)
        if mail:
            mail.is_handling = True
            db.session.add(mail)
