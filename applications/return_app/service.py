# coding: utf-8

from applications.good.service import GoodArgumentExc
from db import db
from applications.return_app.model import Return, ReturnItem, StatusType
from log import debug, error

from services.core import BaseSQLAlchemyModelService

__author__ = 'StasEvseev'


class ReturnService(BaseSQLAlchemyModelService):
    model = Return

    @classmethod
    def create_return(cls, date_start, date_end, provider_id):
        order = Return(
            date_start=date_start, date_end=date_end, provider_id=provider_id)
        db.session.add(order)
        return order

    @classmethod
    def handle_returnitem(cls, full_name, name, number_local, number_global,
                          date, date_to, price_without_NDS, price_with_NDS,
                          remission, count_delivery, count_rem, return_inst):
        from applications.commodity.service import CommodityService
        from applications.good.service import GoodService
        item = ReturnItem()
        item.full_name = full_name
        item.name = name
        item.number_local = number_local
        item.number_global = number_global
        item.date = date
        item.date_to = date_to
        item.price_without_NDS = price_without_NDS
        item.price_with_NDS = price_with_NDS
        item.remission = remission
        item.count_delivery = count_delivery
        item.count_rem = count_rem
        item.return_item = return_inst

        res, comm = CommodityService.get_or_create_commodity(
            name=name)

        if res is False:
            if not number_local and not number_global:
                comm.numeric = False
            db.session.add(comm)
            db.session.flush()

        try:
            res, good = GoodService.get_or_create_commodity_numbers(
                comm.id, number_local, number_global)
        except GoodArgumentExc as exc:
            error(u"При обработке позиций возврата возникла ошибка. " + unicode(
                exc))
            raise

        good.commodity = comm
        good.full_name = full_name
        item.good = good
        db.session.add(good)

        db.session.add(item)

    @classmethod
    def status(cls, return_inst, status):
        debug(u"Смена статуса `возврата` id = '%s' с %s на %s." % (
            return_inst.id, return_inst.status, StatusType[status]))
        old_status = return_inst.status
        return_inst.status = status
        debug(u"Смена статуса `возврата` id = '%s' с %s на %s завершено." % (
            return_inst.id, old_status, StatusType[status]))

    @classmethod
    def set_count_by_id(cls, id, count):
        if count:
            item = ReturnItem.query.get(id)
            item.count = count
            db.session.add(item)

    @classmethod
    def get_mail(cls, id):
        mail = None
        return_inst = cls.get_by_id(id)
        if return_inst.mails_from_return.count() > 0:
            mail = return_inst.mails_from_return[0]
        return mail

    @classmethod
    def set_handling(cls, id):
        mail = cls.get_mail(id)
        if mail:
            mail.is_handling = True
            db.session.add(mail)
