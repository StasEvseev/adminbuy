#coding: utf-8

import os
from collections import namedtuple

from sqlalchemy import desc, func
from applications.waybill.constant import COUNT_ATTR, GOOD_ATTR

from excel.output import PrintInvoice, PATH_TEMPLATE

from db import db

from applications.waybill.models import FROM_MAIL, WayBillItems, WayBill, TYPE, RETAIL, POINTSALE, RECEIVER, RecType, \
    StatusType, FINISH
from log import debug, error
from services import ModelService


WayBillItem = namedtuple('WayBillItem', [GOOD_ATTR, COUNT_ATTR, 'fullname'])


class WayBillServiceException(Exception):
    pass


class WayBillService(object):

    @classmethod
    def check_count(cls, invoice_id, good_id, count, waybill_id):
        waybill = cls.get_by_id(waybill_id)
        from services.mailinvoice import InvoiceService

        if waybill.from_type() == FROM_MAIL:
            count_item = InvoiceService.get_count_item(invoice_id, good_id)
            WayBillItems.query.filter(
                WayBillItems.good_id == good_id
            )
            res = db.session.query(func.sum(WayBillItems.count).label('sum')).join(WayBill).filter(
                WayBill.invoice_id == invoice_id,
                WayBillItems.good_id == good_id)
            res = res.filter(WayBill.id != waybill_id)
            uses_cnt = res.first().sum or 0
            return (uses_cnt + count) <= count_item
        return True

    @classmethod
    def check_exists(cls, invoice_id, receiver_id, pointsale_id, type):
        """
        Проверяем есть ли уже сформированная итоговая накладная по приходной определенной точке или получателю.
        """
        count = 0
        if invoice_id:
            count = cls.count_exists(invoice_id, receiver_id, pointsale_id, type)
        return True if count else False

    @classmethod
    def get_by_id(cls, id):
        return WayBill.query.get(id)

    @classmethod
    def get_items(cls, id):
        return cls.get_by_id(id).items

    #TODO deprecated
    @classmethod
    def get_by_attr(cls, invoice_id, receiver_id, pointsale_id, type):
        """
        Извлекаем накладную из БД по приходной, получателю и типу.
        """
        if not receiver_id or not pointsale_id:
            raise WayBillServiceException(u"No receiver or point sale")
        if invoice_id:
            if ModelService.check_id(receiver_id):
                waybill = WayBill.query.filter(
                    WayBill.invoice_id == invoice_id,
                    WayBill.receiver_id == receiver_id,
                    WayBill.type == type).one()
            else:
                waybill = WayBill.query.filter(
                    WayBill.invoice_id == invoice_id,
                    WayBill.pointsale_id == pointsale_id,
                    WayBill.type == type).one()
            # return count
        else:
            if ModelService.check_id(receiver_id):
                waybill = WayBill.query.filter(
                    WayBill.receiver_id == receiver_id,
                    WayBill.type == type).one()
            else:
                waybill = WayBill.query.filter(
                    WayBill.pointsale_id == pointsale_id,
                    WayBill.type == type).one()
        return waybill

    @classmethod
    def count_exists(cls, invoice_id, receiver_id, pointsale_id, type):
        """
        Возвращаем количество накладных по приходной накладной, получателю и типу.
        """

        if not receiver_id or not pointsale_id:
            raise WayBillServiceException(u"No receiver or point sale")

        if invoice_id:
            if ModelService.check_id(receiver_id):
                count = WayBill.query.filter(
                    WayBill.invoice_id == invoice_id,
                    # WayBill.date == date,
                    WayBill.receiver_id == receiver_id,
                    WayBill.type == type).count()
            else:
                count = WayBill.query.filter(
                    WayBill.invoice_id == invoice_id,
                    # WayBill.date == date,
                    WayBill.pointsale_id == pointsale_id,
                    WayBill.type == type).count()
            return count
        else:
            if ModelService.check_id(receiver_id):
                count = WayBill.query.filter(
                    # WayBill.date == date,
                    WayBill.receiver_id == receiver_id,
                    WayBill.type == type).count()
            else:
                count = WayBill.query.filter(
                    # WayBill.date == date,
                    WayBill.pointsale_id == pointsale_id,
                    WayBill.type == type).count()
            return count

    @classmethod
    def generate_number(cls, date, type):
        """
        Генерация номера для накладной.
        Маска - [порядкой номер для дня] - [тип(1,2)] - [дата полная].
        Пример - 001-1-20122014 - означает первая розничная накладная на дату 20 декабря 2014 года.
        """
        waybill = WayBill.query.filter(
            WayBill.date == date).order_by(desc(WayBill.id)).first()
        if waybill is None:
            return "001-" + str(type) + "-" + date.strftime("%d%m%Y")
        else:
            number = waybill.number
            numbers = number.split("-")
            number = int(numbers[0])
            return "-".join(['%03d' % (number + 1), str(type), numbers[2]])

    #TODO изменить сигнатуру метода
    @classmethod
    def create(cls, pointsale_from_id, invoice_id, date, receiver_id, pointsale_id, type, typeRec, forse=False):
        """
        Создаем или получаем итоговую накладную.
        Сначала проверяем, есть ли уже накладная по параметрам уникальности(приходная накладная, получатели
        (точки или получатель) и тип).
        Если накладной нет, то создаем.
        Если накладная уже есть, генерим исключение. Но если нам передали флаг forse, то извлекаем из БД и возвращаем.
        """
        if not ModelService.check_id(pointsale_from_id):
            raise WayBillServiceException(u"Не выбрана точка отправки.")
        if not ModelService.check_id(receiver_id) and not ModelService.check_id(pointsale_id):
            raise WayBillServiceException(u"No receiver or point sale")

        if pointsale_from_id and ModelService.check_id(pointsale_id) and pointsale_id == pointsale_from_id:
            raise WayBillServiceException(u"Нельзя делать накладную прихода циклической.")

        type = int(type)
        typeRec = int(typeRec)
        if type not in TYPE.keys():
            raise WayBillServiceException(u"Тип накладной указан неверно - %s." % type)
        if typeRec not in RecType.keys():
            raise WayBillServiceException(u"Тип получателя указан неверно - %s." % typeRec)

        waybill = WayBill()
        waybill.invoice_id = invoice_id
        waybill.pointsale_from_id = pointsale_from_id
        waybill.date = date
        if typeRec == POINTSALE:
            if not ModelService.check_id(pointsale_id):
                raise WayBillServiceException(u"Ошибка. Нельзя выбрать тип 'Торговая точка' и 'Оптовика'.")
            waybill.pointsale_id = pointsale_id
            waybill.receiver_id = None
        elif typeRec == RECEIVER:
            if not ModelService.check_id(receiver_id):
                raise WayBillServiceException(u"Ошибка. Нельзя выбрать тип 'Оптовика' и 'Торговую точку'.")
            waybill.receiver_id = receiver_id
            waybill.pointsale_id = None

        waybill.type = type
        waybill.number = cls.generate_number(date, type)
        waybill.typeRec = typeRec
        db.session.add(waybill)
        return waybill

    @classmethod
    def build_retail_items(cls, items):
        """
        Собираем объекты для более удобной обработки из списка словарей.
        """
        try:
            return [WayBillItem(good_id=it[GOOD_ATTR],
                                count=it[COUNT_ATTR] if COUNT_ATTR in it else None,
                                fullname=it['full_name'] if 'full_name' in it else None,
                                ) for it in items]
        except KeyError as exc:
            error(u"Ошибка при сохранении позиций товара. " + unicode(exc))
            raise WayBillServiceException(u"Ошибка при сохранении позиций товара.")

    @classmethod
    def upgrade_items(cls, waybill, items, path_target=None, path=None):
        from applications.price.service import PriceService
        from services import GoodService

        waybill.items.delete()
        db.session.add(waybill)

        for it in items:
            good = GoodService.get_good(it.good_id)
            if waybill.type == RETAIL:
                if not good.price_id or not PriceService.get_price(good.price_id).price_retail:
                    raise WayBillServiceException(
                        u"Товар без розничной цены. %s" % good.full_name)
            else:
                if not good.price_id or not PriceService.get_price(good.price_id).price_gross:
                    raise WayBillServiceException(
                        u"Товар без оптовой цены. %s" % good.full_name)

            if it.count and not WayBillService.check_count(
                    invoice_id=waybill.invoice_id, waybill_id=waybill.id, good_id=it.good_id,
                    count=int(it.count)):
                raise WayBillServiceException(
                    u"Недостаточно товара %s" % good.full_name
                )

            retail_item = WayBillItems(
                good_id=good.id, waybill=waybill, count=it.count if it.count else None)
            db.session.add(retail_item)

    @classmethod
    def status(cls, waybill, status):
        from applications.point_sale.service import PointSaleService
        debug(u"Смена статуса `накладной` id = '%s' с %s на %s." % (waybill.id, waybill.status, StatusType[status]))

        if status == FINISH:
            debug(u"Финальный статус `накладной`.")

            from_point = waybill.pointsale_from

            if waybill.receiver:
                debug(u"Пересчет кол-ва товаром на точке отправителе id = '%s'" % from_point.id)
                for item in waybill.items:
                    PointSaleService.sync_good_increment(from_point.id, item.good_id, item.count * -1 if item.count else 0)
            else:
                to_point = waybill.pointsale
                debug(u"Пересчет кол-ва товаров на точке отправителе id = '%s' и точке получаете id = '%s'." % (
                    from_point.id, to_point.id))
                for item in waybill.items:
                    PointSaleService.sync_good_increment(from_point.id, item.good_id, item.count * -1 if item.count else 0)
                    PointSaleService.sync_good_increment(to_point.id, item.good_id, item.count if item.count else 0)
            debug(u"Пересчет кол-ва товаров завершен.")
        old_status = waybill.status
        waybill.status = status
        debug(u"Смена статуса `накладной` id = '%s' с %s на %s завершено." % (
            waybill.id, old_status, StatusType[status]))