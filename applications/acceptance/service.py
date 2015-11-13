#coding: utf-8

__author__ = 'StasEvseev'

from sqlalchemy import asc
from sqlalchemy.orm.exc import NoResultFound
from applications.acceptance.constant import ITEM_ID_ATTR, COUNT_ATTR, GOOD_ATTR, PRICE_POST_ATTR, PRICE_RETAIL_ATTR, \
    PRICE_GROSS_ATTR, GOOD_OBJ_ATTR, GOOD_ID_ATTR
from applications.acceptance.model import Acceptance, StatusType, AcceptanceItems, IN_PROG, VALIDATED, MAIL, NEW, DRAFT

from db import db
from log import debug
from models.invoiceitem import InvoiceItem


class AcceptanceService(object):

    @classmethod
    def get_by_invoice_id(cls, invoice_id):
        try:
            return Acceptance.query.filter(
                Acceptance.invoice_id == invoice_id
            ).one()
        except NoResultFound:
            pass

    @classmethod
    def get_all(cls):
        return Acceptance.query.all()

    @classmethod
    def get_by_id(cls, id):
        return Acceptance.query.get(id)

    @classmethod
    def get_item(cls, id):
        return AcceptanceItems.query.get(id)

    @classmethod
    def update_fact_count(cls, acceptance, items):
        debug(u"Обновление фактического кол-ва по почте `прихода` id = '%s' "
              u"начато." % acceptance.id)
        for item in items:
            id = item[ITEM_ID_ATTR]
            fact_count = item[COUNT_ATTR]
            if fact_count:
                it = cls.get_item(id)
                it.fact_count = fact_count
                db.session.add(it)
        debug(u"Обновление фактического кол-ва по почте `прихода` id = '%s' "
              u"завершено." % acceptance.id)

    @classmethod
    def update_fact_count_custom(cls, acceptance, items):
        debug(u"Обновление фактического кол-ва по новой `прихода` id = '%s' "
              u"начато." % acceptance.id)
        from services.mailinvoice import InvoiceService
        from applications.good.service import GoodService
        invoice = acceptance.invoice
        acceptance.items.delete()
        invoice.items.delete()
        for item in items:
            good_id = item[GOOD_OBJ_ATTR][GOOD_ID_ATTR]
            fact_count = item[COUNT_ATTR]
            price_post = item[PRICE_POST_ATTR]
            price_retail = item[PRICE_RETAIL_ATTR]
            price_gross = item[PRICE_GROSS_ATTR]
            good = GoodService.get_good(good_id)
            InvoiceService.handle_invoiceitem(
                invoice=invoice, good=good, fact_count=fact_count,
                price_with_NDS=price_post, full_name=None, name=None,
                number_local=None, number_global=None, count_order=None,
                count_postorder=None, count=fact_count,
                price_without_NDS=None, sum_NDS=None, sum_with_NDS=None,
                thematic=None, count_whole_pack=None, placer=None,
                rate_NDS=None, sum_without_NDS=None, price_retail=price_retail,
                price_gross=price_gross)
            ac_it = AcceptanceItems()
            ac_it.good_id = good_id
            ac_it.acceptance = acceptance
            ac_it.count = fact_count
            ac_it.fact_count = fact_count
            db.session.add(ac_it)
        debug(u"Обновление фактического кол-ва по новой `прихода` id = '%s' "
              u"завершено." % acceptance.id)

    @classmethod
    def get_or_create_by_invoice_pointsale(cls, invoice_id, pointsale_id):
        """
        Получаем либо создаем приемку товара.
        """
        try:
            acceptance = Acceptance.query.filter(
                Acceptance.invoice_id == invoice_id,
                Acceptance.pointsale_id == pointsale_id).one()
            is_new = False
        except NoResultFound:
            acceptance = Acceptance()
            acceptance.invoice_id = invoice_id
            acceptance.pointsale_id = pointsale_id
            db.session.add(acceptance)
            is_new = True

        return is_new, acceptance

    @classmethod
    def status(cls, acceptance, status):
        from applications.point_sale.service import PointSaleService
        from applications.price.service import PriceService, DataToUpdatePrice
        debug(u"Смена статуса `прихода` id = '%s' с %s на %s." % (
            acceptance.id, acceptance.status, StatusType[status]))

        if status == DRAFT:
            if acceptance.type == NEW:
                debug(u"Переход `прихода` id = '%s' в статус 'Черновик' и "
                      u"типом 'Новая' сопровождается удалением накладной."
                      % acceptance.id)
                acceptance.items.delete()
                acceptance.invoice.items.delete()
                db.session.delete(acceptance.invoice)

        if status == IN_PROG:
            if acceptance.type == MAIL:
                cls.initial_acceptance_from_mail(acceptance)
            elif acceptance.type == NEW:
                cls.initial_acceptance_from_custom(acceptance)

        if status == VALIDATED:
            if acceptance.type == MAIL:
                for item in acceptance.items:
                    if item.fact_count:
                        PointSaleService.sync_good_increment(
                            acceptance.pointsale_id, item.good_id,
                            item.fact_count)
            elif acceptance.type == NEW:
                invoice = acceptance.invoice
                for item in invoice.items:
                    good = item.good

                    PriceService.create_or_update(good, DataToUpdatePrice(
                        id_commodity=good.commodity_id,
                        price_retail=item.price_retail,
                        price_gross=item.price_gross,
                        price_prev=None,
                        price_post=item.price_with_NDS,
                        NDS=None,
                        number_local=good.number_local,
                        number_global=good.number_global,
                        invoice=invoice))
                    if item.fact_count:
                        PointSaleService.sync_good_increment(
                            acceptance.pointsale_id, item.good_id,
                            item.fact_count)
        old_status = acceptance.status
        acceptance.status = status
        debug(u"Смена статуса `прихода` id = '%s' с %s на %s завершено." % (
            acceptance.id, old_status, StatusType[status]))

    @classmethod
    def initial_acceptance_from_custom(cls, acceptance):
        debug(u"Инициализация по новой `прихода` id = '%s' начата."
              % acceptance.id)
        from services.mailinvoice import InvoiceService
        invoice = InvoiceService.create_invoice(
            number=InvoiceService.generate_number(acceptance.date),
            date=acceptance.date, provider=acceptance.provider
        )
        acceptance.invoice = invoice
        debug(u"Инициализация по новой `прихода` id = '%s' завершена."
              % acceptance.id)

    @classmethod
    def initial_acceptance_from_mail(cls, acceptance):
        debug(u"Инициализация по почте `прихода` id = '%s' начата."
              % acceptance.id)
        invoice = acceptance.invoice
        items = invoice.items.order_by(asc(InvoiceItem.id))
        debug(u"Удаляем позиции прихода id = '%s'." % acceptance.id)
        acceptance.items.delete()
        debug(u"Создаем новые позиции прихода id = '%s' из накладной."
              % acceptance.id)
        for item in items:
            ac_it = AcceptanceItems()
            ac_it.good_id = item.good_id
            ac_it.acceptance = acceptance
            ac_it.count = item.count
            db.session.add(ac_it)
        debug(u"Инициализация по почте `прихода` id = '%s' завершена."
              % acceptance.id)