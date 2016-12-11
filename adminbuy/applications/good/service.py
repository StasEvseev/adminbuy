# coding: utf-8

from collections import namedtuple

from sqlalchemy import not_
from sqlalchemy.orm.exc import NoResultFound

from adminbuy.applications.invoice.models import InvoiceItem

from .model import Good


GoodStub = namedtuple('GoodStub',
                      ['id_price', 'id_commodity', 'full_name', 'count',
                       'barcode'])


class GoodServiceException(Exception):
    pass


class GoodArgumentExc(GoodServiceException):
    pass


class GoodNotPriceException(GoodServiceException):
    pass


class GoodNotFountException(GoodServiceException):
    pass


class GoodService(object):

    @classmethod
    def get_goods(cls):
        return Good.query.all()

    @classmethod
    def get_or_create_commodity_numbers(
            cls, commodity_id, number_local=None, number_global=None, id=None):
        from adminbuy.applications.commodity.service import CommodityService
        commodity = CommodityService.get_by_id(commodity_id)

        if commodity.numeric:
            if not number_local and not number_global:
                raise GoodArgumentExc(
                    u"Для номерного товара '%s' не указаны номера" %
                    unicode(commodity.name))

        if commodity.numeric is False:
            if number_local or number_global:
                raise GoodArgumentExc(
                    u"Для безномерного товара '%s' нельзя указывать номера" %
                    unicode(commodity.name))

        try:
            if id:
                good = Good.query.filter(
                    Good.commodity_id == commodity_id,
                    Good.number_local == number_local,
                    Good.number_global == number_global,
                    not_(Good.id == id)).one()
            else:
                good = Good.query.filter(
                    Good.commodity_id == commodity_id,
                    Good.number_local == number_local,
                    Good.number_global == number_global).one()
        except NoResultFound:
            if id:
                return False, Good.query.get(id)
            else:
                return False, Good(commodity_id=commodity_id,
                                   number_local=number_local,
                                   number_global=number_global)
        else:
            return True, good

    @classmethod
    def get_good_exlude_invoice(cls, invoice_id):
        return Good.query.join(InvoiceItem).filter(
            InvoiceItem.invoice_id != invoice_id).all()

    @classmethod
    def get_good(cls, id):
        good = Good.query.get(id)
        if not good:
            raise GoodNotFountException(u"Не найдено записи в БД")

        return good

    @classmethod
    def get_price(cls, good_id):
        from adminbuy.applications.price.service import PriceService
        good = cls.get_good(good_id)
        if good.price_id:
            return PriceService.get_price(good.price_id)

    @classmethod
    def full_name(cls, good):
        return cls.generate_name(good.commodity.name, good.number_local,
                                 good.number_global)

    @classmethod
    def generate_name(cls, name, number_local=None, number_global=None):
        numeric = True if number_local and number_global else False
        if numeric:
            full_name = name + u" №" + unicode(number_local) + u"(" + unicode(
                number_global) + u")"
        else:
            full_name = name
        return full_name

    @classmethod
    def update_good(cls, session, id, barcode, commodity_id, number_local=None,
                    number_global=None, price_id=None,
                    full_name=None):
        good = cls.get_good(id)
        good.barcode = barcode
        good.commodity_id = commodity_id
        good.number_local = number_local
        good.number_global = number_global
        good.price_id = price_id

        if not full_name:
            full_name = GoodService.full_name(good)
        good.full_name = full_name

        session.add(good)
