#coding: utf-8

__author__ = 'StasEvseev'

import redis
from sqlalchemy import desc
from applications.good.service import GoodService, GoodArgumentExc

from log import debug, error

from db import db

from models.invoice import Invoice
from models.invoiceitem import InvoiceItem
from applications.provider_app.service import ProviderService
from applications.mails.model import Mail
from applications.mails.action import get_count_mails, NotConnect, MailHepls, mark_as_unseen


class MailInvoiceException(Exception):
    pass


class InvoiceService(object):
    """
    Сервисный слой работы с накладными.
    """

    class InvoiceServiceException(Exception):
        pass

    @classmethod
    def generate_number(cls, date):
        """
        Генерация номера для накладной.
        Маска - [порядкой номер для дня] - [тип(1,2)] - [дата полная].
        Пример - 001-1-20122014 - означает первая розничная накладная на дату 20 декабря 2014 года.
        """
        invoice = Invoice.query.filter(
            Invoice.date==date).order_by(desc(Invoice.id)).first()
        if invoice is None:
            return "001-" + date.strftime("%d%m%Y")
        else:
            number = invoice.number
            numbers = number.split("-")
            number = int(numbers[0])
            return "-".join(['%03d' % (number + 1), numbers[1]])


    @classmethod
    def get_by_id(cls, id):
        return Invoice.query.get(id)

    @classmethod
    def get_all(cls):
        """
        Получаем все накладные
        """
        return Invoice.query.all()

    @classmethod
    def get_from(cls, from_id):
        """
        Возвращаем все накладные с id больше переданного.
        """
        return Invoice.query.filter(Invoice.id > from_id)

    @classmethod
    def get_count_items(cls, invoice_id):
        """
        Возвращаем количество позиций в накладной.
        """
        return InvoiceItem.query.filter(InvoiceItem.invoice_id == invoice_id).count()

    @classmethod
    def get_items(cls, invoice_id):
        """
        Получаем позиции накладной по id
        """
        return InvoiceItem.query.filter(
            InvoiceItem.invoice_id==invoice_id).order_by(InvoiceItem.id).all()

    @classmethod
    def get_items_acceptance(cls, acc_id, remain=True):
        from applications.point_sale.service import PointSaleService
        from applications.acceptance.service import AcceptanceService
        from applications.waybill.service import WayBillService
        acceptance = AcceptanceService.get_by_id(acc_id)
        pointsale = acceptance.pointsale

        def get_count_remain(remain, item, pointsale_id):
            if remain:
                return PointSaleService.item_to_pointsale_good(pointsale.id, item.good_id).count \
                    if PointSaleService.item_to_pointsale_good(pointsale.id, item.good_id) else ""
            else:
                return item.count

        if acceptance.invoice:

            return [{
                "id": item.id,
                "full_name": item.full_name,
                "good_id": item.good_id,
                "price_without_NDS": item.price_without_NDS,
                "price_with_NDS": item.price_with_NDS,
                "price_retail": GoodService.get_price(item.good_id).price_retail if GoodService.get_price(item.good_id) else "",
                "price_gross": GoodService.get_price(item.good_id).price_gross if GoodService.get_price(item.good_id) else "",
                "count": get_count_remain(remain, item, pointsale.id),
                "fact_count": item.fact_count

            } for item in cls.get_items(invoice_id=acceptance.invoice_id)]

        elif acceptance.waybill_crud:
            return [{
                "id": item.id,
                "full_name": item.good.full_name,
                "good_id": item.good_id,
                "price_retail": GoodService.get_price(item.good_id).price_retail if GoodService.get_price(item.good_id) else "",
                "price_gross": GoodService.get_price(item.good_id).price_gross if GoodService.get_price(item.good_id) else "",
                "count": get_count_remain(remain, item, pointsale.id),

            } for item in WayBillService.get_items(acceptance.waybill_id)]

    @classmethod
    def get_item_by_id(cls, id):
        return InvoiceItem.query.get(id)

    @classmethod
    def get_item_by_invoice_good(cls, invoice_id, good_id):
        return InvoiceItem.query.filter(
            InvoiceItem.invoice_id == invoice_id,
            InvoiceItem.good_id == good_id
        ).first()

    @classmethod
    def get_count_item(cls, invoice_id, good_id):
        return cls.get_item_by_invoice_good(invoice_id, good_id).count

    @classmethod
    def get_item_to_acceptance(cls, invoice_id, acceptance_id):
        from applications.point_sale.service import PointSaleService
        from applications.acceptance.service import AcceptanceService
        acceptance = AcceptanceService.get_by_id(acceptance_id)
        pointsale = acceptance.pointsale

        return [{
            "id": item.id,
            "full_name": item.full_name,
            "good_id": item.good_id,
            "price_retail": GoodService.get_price(item.good_id).price_retail if GoodService.get_price(item.good_id) else "",
            "price_gross": GoodService.get_price(item.good_id).price_gross if GoodService.get_price(item.good_id) else "",
            "count": PointSaleService.item_to_pointsale_good(pointsale.id, item.good_id).count if PointSaleService.item_to_pointsale_good(pointsale.id, item.good_id) else "",

        } for item in cls.get_items(invoice_id=invoice_id)]

    @classmethod
    def update_fact_count_items(cls, id, fact_count):
        """
        Обновление фактического количества у позиций накладной
        """
        invoiceitem = InvoiceItem.query.get(id)
        invoiceitem.fact_count = fact_count or None
        db.session.add(invoiceitem)

    @classmethod
    def create_invoice(cls, number, date, provider,
                            sum_without_NDS=None, sum_with_NDS=None,
                            sum_NDS=None, weight=None, responsible=None):
        invmodel = Invoice(
           number=number, date=date,
           sum_without_NDS=sum_without_NDS, sum_with_NDS=sum_with_NDS,
           sum_NDS=sum_NDS, weight=weight, responsible=responsible)
        if provider:
            invmodel.provider = provider
        db.session.add(invmodel)
        return invmodel

    @classmethod
    def save_from_json(cls, date, items, provider_id=None, invoice=None):
        """
        Сохраняем накладную с позициями.

        Для редактирования надо передать инстанс накладной в переменную invoice.
        """
        from applications.price.service import DataToUpdatePrice, PriceService
        from applications.point_sale.service import PointSaleService
        try:
            if invoice:
                invmodel = invoice
            else:
                provider = ProviderService.get_by_id(provider_id)

                invmodel = InvoiceService.create_invoice(
                    number=InvoiceService.generate_number(date), date=date,provider=provider,
                    sum_without_NDS=None, sum_with_NDS=None,
                    sum_NDS=None, weight=None, responsible=None)

                db.session.add(invmodel)

            if invoice:
                pointsale = invoice.acceptance.pointsale
                for item in invmodel.items:
                    pointsale_item = PointSaleService.item_to_pointsale_good(
                        pointsale.id, item.good_id)
                    pointsale_item.count -= item.count
                    db.session.add(pointsale_item)
                invmodel.items.delete()
                db.session.add(invmodel)

            for item in items:
                good = GoodService.get_good(item['good_id'])
                name = good.commodity.name
                number_local = good.number_local
                number_global = good.number_global
                full_name = GoodService.generate_name(name, number_local, number_global)

                invoice = invmodel
                count_order= None
                count_postorder = None
                count = item['count_invoice'] if 'count_invoice' in item else None
                price_without_NDS = item['price_pre'] if 'price_pre' in item else None
                price_with_NDS = item['price_post'] if 'price_post' in item else None
                sum_without_NDS = None
                sum_NDS = None
                rate_NDS = item['NDS'] if 'NDS' in item else None
                sum_with_NDS = None
                thematic = None
                count_whole_pack = None
                placer = None
                fact_count = None

                cls.handle_invoiceitem(full_name, name, number_local, number_global, invoice, count_order, count_postorder,
                                       count, price_without_NDS, price_with_NDS, sum_without_NDS, sum_NDS, rate_NDS, sum_with_NDS,
                                       thematic, count_whole_pack, placer, good, fact_count)

                if 'price_retail' in item or 'price_gross' in item:
                    PriceService.create_or_update(good, DataToUpdatePrice(
                        id_commodity=good.commodity_id, price_retail=item['price_retail'], price_gross=item['price_gross'],
                        price_prev=item['price_prev'] if 'price_prev' in item else None,
                        price_post=item['price_post'],
                        NDS=item['NDS'] if 'NDS' in item else None,
                        number_local=number_local, number_global=number_global,
                        invoice=invmodel))

        except Exception as exc:
            db.session.rollback()
            error(unicode(exc))
            raise InvoiceService.InvoiceServiceException(unicode(exc))
        else:
            db.session.commit()
            return invmodel

    @classmethod
    def handle_invoiceitem(cls, full_name, name, number_local, number_global, invoice, count_order,
                           count_postorder, count, price_without_NDS, price_with_NDS, sum_without_NDS,
                           sum_NDS, rate_NDS, sum_with_NDS, thematic, count_whole_pack, placer, good=None,
                           fact_count=None, price_retail=None, price_gross=None):
        """
        Обработка позиции накладной.

        Сохраняем в БД позицию.
        Создаем товар в системе.
        """
        from applications.commodity.service import CommodityService
        invitem = InvoiceItem()

        invitem.full_name=full_name
        invitem.count_order=count_order
        invitem.count_postorder=count_postorder
        invitem.count=count
        invitem.price_without_NDS=price_without_NDS
        invitem.price_with_NDS=price_with_NDS
        invitem.sum_without_NDS=sum_without_NDS
        invitem.sum_with_NDS=sum_with_NDS
        invitem.sum_NDS=sum_NDS
        invitem.rate_NDS=rate_NDS
        invitem.count_whole_pack=count_whole_pack
        invitem.placer=placer
        invitem.invoice=invoice
        invitem.price_gross = price_gross
        invitem.price_retail = price_retail

        if good:
            invitem.good = good
            invitem.name = good.commodity.name
            invitem.number_local = good.number_local
            invitem.number_global = good.number_global
            invitem.thematic=good.commodity.thematic
            if fact_count:
                invitem.fact_count = fact_count
        else:
            invitem.name=name
            invitem.number_local=number_local
            invitem.number_global=number_global
            invitem.thematic=thematic
            res, comm = CommodityService.get_or_create_commodity(
                name=name, thematic=thematic)

            if res is False:
                if not number_local and not number_global:
                    comm.numeric = False
                db.session.add(comm)
                db.session.flush()
            try:
                res, good = GoodService.get_or_create_commodity_numbers(comm.id, number_local, number_global)
            except GoodArgumentExc as exc:
                error(u"При обработке позиций накладной возникла ошибка. " + unicode(exc))
                raise

            good.commodity = comm
            good.full_name = full_name
            invitem.good = good
            db.session.add(good)

        db.session.add(invitem)


class MailInvoiceService(object):

    @classmethod
    def get_invoice(cls, invoice_id):
        return Invoice.query.get(invoice_id)

    @classmethod
    def get_mail(cls, id):
        return Mail.query.get(id)

    @classmethod
    def handle(cls, mail):
        if mail.is_handling is False:
            mail.is_handling = True
            print "PUbLISH"
            r = redis.StrictRedis(host='localhost', port=6379, db=0)
            r.publish("mail_handle", mail.id)

    @classmethod
    def handle_mail(cls):
        """
        Метод обрабатывает почтовый ящик
        """
        from applications.provider_app.service import ProviderService
        res = []
        debug(u"Начало проверки почты")
        emails = ProviderService.get_all_emails()
        debug(u"Найдено %d почтовых ящиков отправителей", len(emails))
        try:
            count = cls.get_count_new_mails(emails)
        except Exception as err:
            error(u"Произошла ошибка при обработке почты. %s" % unicode(err))
            raise MailInvoiceException(err)
        debug(u"Найдено %d новых писем", count)
        if count > 0 and emails > 0:
            ids = []
            try:
                ids, mails = MailHepls.get_mails(emails)
                for _from in mails:
                    provider = ProviderService.get_provider_by_email(_from)
                    mailss = mails[_from]
                    for mail in mailss:
                        ml = Mail(
                            title=mail.title, date=mail.date_, text=mail.text,
                            from_=mail.from_, to=mail.to_, files=mail.files)
                        ml.provider = provider
                        db.session.add(ml)
                        db.session.commit()
                        try:
                            print "PUBLIC new mail"
                            r = redis.StrictRedis(host='localhost', port=6379, db=0)
                            r.publish("new mail", "")
                        except Exception as exc:
                            error(u"Не удалось подключиться к редису")

                        res.append(ml)
            except GoodArgumentExc as exc:
                mark_as_unseen(ids)
                raise MailInvoiceException(exc)
            except Exception as err:
                try:
                    mark_as_unseen(ids)
                except Exception as err:
                    error(u"Произошла ошибка при пометке писем как непрочитанных. %s", unicode(err))
                    raise
                error(u"Произошла ошибка при обработке почты. %s", unicode(err))
                raise MailInvoiceException(err)
        debug(u"Конец проверки почты")
        return res

    @classmethod
    def get_new_mails(cls, emails=None):
        res = []
        if emails is None:
            return Mail.query.filter(Mail.is_handling==False)
        else:
            for email in emails:
                res.append(Mail.query.filter(Mail.from_==email))
        return res

    @classmethod
    def get_count_new_mails(cls, emails):
        count = 0
        for email in emails:
            try:
                count += get_count_mails(email)
            except NotConnect as err:
                raise MailInvoiceException(err)
        return count