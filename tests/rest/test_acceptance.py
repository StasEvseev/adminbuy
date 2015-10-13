#coding: utf-8

__author__ = 'StasEvseev'

from datetime import datetime, date
from applications.acceptance.constant import GOOD_ATTR, COUNT_ATTR, ITEM_ID_ATTR, PRICE_GROSS_ATTR, PRICE_POST_ATTR, \
    PRICE_RETAIL_ATTR, GOOD_ID_ATTR, GOOD_OBJ_ATTR
from applications.acceptance.model import MAIL, NEW, Acceptance, AcceptanceItems, IN_PROG, VALIDATED

from applications.good.model import Good
from applications.price.model import Price, PriceParish
from models.invoice import Invoice
from models.invoiceitem import InvoiceItem
from applications.point_sale.models import PointSaleItem
from tests import BaseTestCase
from tests.helpers import Generator
from tests.helpers.suits.acceptance import AcceptanceSuite
from tests.helpers.suits.application import ApplicationSuite
from tests.helpers.suits.invoice import MailInvoiceTestSuite
from tests.helpers.suits.pointsale import PointSaleSuite
from tests.helpers.suits.providersuit import ProviderTestSuite


class AcceptanceTest(BaseTestCase):
    def set_up(self):
        self.FILE_NAME = "20141020_2IAEW4.xlsx"

        self.acceptance_suite = AcceptanceSuite(self.client, self.application)

        self.pointsale_suite = PointSaleSuite(self.client, self.application)

        self.application_suite = ApplicationSuite(self.client, self.application)

        self.provider_suite = ProviderTestSuite(self.client, self.application)
        self.test_provider_id, _, _, _ = self.provider_suite.create_test_provider()

        self.invoice_suite = MailInvoiceTestSuite(self.client, self.application)
        with self.application.app_context():
            pointsale = self.pointsale_suite.create_test_pointsale(name=u"ШШК", address=u"Наб. Челны")
            self.pointsale_id = pointsale.id

    def invoice_(self):
        # with self.application.app_context():
        self.invoice_suite.handle_invoice(datetime=datetime.now(), file_name=self.FILE_NAME, mail_id=1)
        self.invoice_id = Invoice.query.first().id

    def price_to_good(self, good_id):
        return Good.query.filter(
            Good.id == good_id
        ).one().price

    def priceparish_to_good(self, good_id):
        good = Good.query.get(good_id)
        return PriceParish.query.filter(
            PriceParish.commodity_id == good.commodity_id,
            PriceParish.number_local_from == good.number_local,
            PriceParish.number_global_from == good.number_global
        )

    def invoice_count(self):
        return Invoice.query.count()

    def acceptance_count(self):
        return Acceptance.query.count()

    def acceptance_items(self, id):
        return AcceptanceItems.query.filter(
            AcceptanceItems.acceptance_id == id
        )

    def acceptance_item(self, id):
        return AcceptanceItems.query.filter(
            AcceptanceItems.id == id
        ).one()

    def pointsale_items(self, id):
        return PointSaleItem.query.filter(
            PointSaleItem.pointsale_id == id
        )

    def invoice_items(self, id):
        return InvoiceItem.query.filter(
            InvoiceItem.invoice_id == id
        )

    def success_stories_mail(self, date):
        self.invoice_()
        return self.acceptance_suite.create(date=date, type=MAIL, invoice_id=self.invoice_id,
                                            pointsale_id=self.pointsale_id)


class AcceptanceFromMail(AcceptanceTest):

    def testItemsAcceptanceFromMail(self):
        date = Generator.generate_date()

        with self.application.app_context():
            resp = self.success_stories_mail(date)
            acc_id = 1
            inv_items = self.invoice_items(self.invoice_id)
            items = self.acceptance_items(acc_id)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.acceptance_count(), 1)
            self.assertEqual(items.count(), 0)

            resp = self.acceptance_suite.acceptance_status(acc_id, IN_PROG)
            self.assertEqual(resp.status_code, 200)
            items = self.acceptance_items(acc_id)
            self.assertEqual(self.acceptance_count(), 1)
            self.assertEqual(items.count(), 41)
            inv_items.session.autocommit = True
            inv_itemss = list(inv_items)
            inv_items.session.rollback()
            itemss = list(items)
            items.session.rollback()

            for item, inv_item in zip(itemss, inv_itemss):
                self.assertEqual(item.count, inv_item.count)
                self.assertIsNone(item.fact_count)

            items_acc = []
            for item in itemss[:10]:
                items_acc.append(
                    {ITEM_ID_ATTR: item.id, GOOD_ATTR: item.good_id, COUNT_ATTR: item.count})

            items_acc.append({ITEM_ID_ATTR: itemss[10].id, GOOD_ATTR: itemss[10].good_id, COUNT_ATTR: itemss[10].count})

            resp = self.acceptance_suite.update_items(acc_id, items=items_acc)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.acceptance_items(acc_id).count(), 41)

            resp = self.acceptance_suite.acceptance_status(acc_id, VALIDATED)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.pointsale_items(self.pointsale_id).count(), 11)

            for item_acc in items_acc:
                item = self.acceptance_item(item_acc['id'])
                self.assertEqual(item.count, item_acc[COUNT_ATTR])

            # for item_acc, item_p in zip(self.acceptance_items(acc_id), self.pointsale_items(self.pointsale_id)):
            #     self.assertEqual(item_acc.count, item_p.count)

    def tear_down(self):
        pass


class AcceptanceCustom(AcceptanceTest):

    def testFromCustom(self):
        PRICE_R_G_1 = 12.0
        PRICE_G_G_1 = 10.0
        PRICE_R_G_3 = 15.0
        PRICE_G_G_3 = 12.0
        good_id = self.application_suite.good(u"ЛТД", '1', '2', PRICE_R_G_1, PRICE_G_G_1)
        good_id_2 = self.application_suite.good(u"ЛТД", '2', '3', PRICE_R_G_1, PRICE_G_G_1)
        good_id_3 = self.application_suite.good(u"Вечерние Челны", '1', '2', PRICE_R_G_3, PRICE_G_G_3)
        date = Generator.generate_date()
        with self.application.app_context():

            count_pp_good_1 = self.priceparish_to_good(good_id).count()
            count_pp_good_2 = self.priceparish_to_good(good_id_2).count()
            count_pp_good_3 = self.priceparish_to_good(good_id_3).count()

            resp = self.acceptance_suite.create(date=date, pointsale_id=self.pointsale_id, type=NEW,
                                                provider_id=self.test_provider_id)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.acceptance_count(), 1)
            self.assertEqual(self.invoice_count(), 0)

            acc_id = 1
            items = self.acceptance_items(acc_id)
            p_items = self.pointsale_items(self.pointsale_id)

            self.assertEqual(items.count(), 0)
            self.assertEqual(p_items.count(), 0)

            resp = self.acceptance_suite.acceptance_status(acc_id, IN_PROG)
            inv_id = 1
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.acceptance_count(), 1)
            self.assertEqual(self.invoice_count(), 1)

            items = self.acceptance_items(acc_id)
            p_items = self.pointsale_items(self.pointsale_id)
            i_items = self.invoice_items(inv_id)

            self.assertEqual(items.count(), 0)
            self.assertEqual(p_items.count(), 0)
            self.assertEqual(i_items.count(), 0)

            resp = self.acceptance_suite.update_new_items(acc_id, items=[
                {GOOD_OBJ_ATTR: {GOOD_ID_ATTR: good_id}, COUNT_ATTR: 15, PRICE_POST_ATTR: 8.0,
                 PRICE_RETAIL_ATTR: PRICE_R_G_1 + 1.0, PRICE_GROSS_ATTR: PRICE_G_G_1},
                {GOOD_OBJ_ATTR: {GOOD_ID_ATTR: good_id_3}, COUNT_ATTR: 5, PRICE_POST_ATTR: 9.5,
                 PRICE_RETAIL_ATTR: PRICE_R_G_3, PRICE_GROSS_ATTR: PRICE_G_G_3}
            ])
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.acceptance_count(), 1)
            self.assertEqual(self.invoice_count(), 1)
            self.assertEqual(self.priceparish_to_good(good_id).count(), count_pp_good_1)
            self.assertEqual(self.priceparish_to_good(good_id_3).count(), count_pp_good_3)
            self.assertEqual(self.price_to_good(good_id).price_retail, PRICE_R_G_1)
            self.assertEqual(self.price_to_good(good_id).price_gross, PRICE_G_G_1)
            self.assertEqual(self.price_to_good(good_id_3).price_retail, PRICE_R_G_3)
            self.assertEqual(self.price_to_good(good_id_3).price_gross, PRICE_G_G_3)

            items = self.acceptance_items(acc_id)
            p_items = self.pointsale_items(self.pointsale_id)
            i_items = self.invoice_items(inv_id)

            self.assertEqual(items.count(), 2)
            self.assertEqual(p_items.count(), 0)
            self.assertEqual(i_items.count(), 2)

            resp = self.acceptance_suite.update_new_items(acc_id, items=[
                {GOOD_OBJ_ATTR: {GOOD_ID_ATTR: good_id}, COUNT_ATTR: 15, PRICE_POST_ATTR: 8.0,
                 PRICE_RETAIL_ATTR: PRICE_R_G_1 + 1.0, PRICE_GROSS_ATTR: PRICE_G_G_1},
                {GOOD_OBJ_ATTR: {GOOD_ID_ATTR: good_id_3}, COUNT_ATTR: 5, PRICE_POST_ATTR: 9.5,
                 PRICE_RETAIL_ATTR: PRICE_R_G_3, PRICE_GROSS_ATTR: PRICE_G_G_3}
            ])
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.acceptance_count(), 1)
            self.assertEqual(self.invoice_count(), 1)
            self.assertEqual(self.priceparish_to_good(good_id).count(), count_pp_good_1)
            self.assertEqual(self.priceparish_to_good(good_id_3).count(), count_pp_good_3)
            self.assertEqual(self.price_to_good(good_id).price_retail, PRICE_R_G_1)
            self.assertEqual(self.price_to_good(good_id).price_gross, PRICE_G_G_1)
            self.assertEqual(self.price_to_good(good_id_3).price_retail, PRICE_R_G_3)
            self.assertEqual(self.price_to_good(good_id_3).price_gross, PRICE_G_G_3)

            items = self.acceptance_items(acc_id)
            p_items = self.pointsale_items(self.pointsale_id)
            i_items = self.invoice_items(inv_id)

            self.assertEqual(items.count(), 2)
            self.assertEqual(p_items.count(), 0)
            self.assertEqual(i_items.count(), 2)

            resp = self.acceptance_suite.acceptance_status(acc_id, VALIDATED)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.acceptance_count(), 1)
            self.assertEqual(self.invoice_count(), 1)
            self.assertEqual(self.priceparish_to_good(good_id).count(), count_pp_good_1 + 1)
            self.assertEqual(self.priceparish_to_good(good_id_3).count(), count_pp_good_3 + 1)
            self.assertEqual(self.price_to_good(good_id).price_retail, PRICE_R_G_1 + 1.0)
            self.assertEqual(self.price_to_good(good_id).price_gross, PRICE_G_G_1)
            self.assertEqual(self.price_to_good(good_id_3).price_retail, PRICE_R_G_3)
            self.assertEqual(self.price_to_good(good_id_3).price_gross, PRICE_G_G_3)

            items = self.acceptance_items(acc_id)
            p_items = self.pointsale_items(self.pointsale_id)
            i_items = self.invoice_items(inv_id)

            self.assertEqual(items.count(), 2)
            self.assertEqual(p_items.count(), 2)
            self.assertEqual(i_items.count(), 2)


class AcceptanceCrush(AcceptanceTest):

    def testCrushFromMail(self):
        date = Generator.generate_date()
        with self.application.app_context():
            count = self.acceptance_count()
            self.invoice_()
            #Не выбран Тип
            resp = self.acceptance_suite.create(date=date, invoice_id=self.invoice_id, pointsale_id=self.pointsale_id)
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(self.acceptance_count(), count)

            resp = self.acceptance_suite.create(date=date, provider_id=self.test_provider_id, pointsale_id=self.pointsale_id)
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(self.acceptance_count(), count)

            #Несуществующий тип
            resp = self.acceptance_suite.create(date=date, type=3, invoice_id=self.invoice_id,
                                                pointsale_id=self.pointsale_id)
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(self.acceptance_count(), count)
            #Тип "Из почты", а накладная не выбрана
            resp = self.acceptance_suite.create(date=date, type=MAIL, pointsale_id=self.pointsale_id,
                                                provider_id=self.test_provider_id)
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(self.acceptance_count(), count)
            #Тип "Новая", а поставщик не выбран
            resp = self.acceptance_suite.create(date=date, type=NEW, pointsale_id=self.pointsale_id,
                                                invoice_id=self.invoice_id)
            self.assertEqual(resp.status_code, 400)
            self.assertEqual(self.acceptance_count(), count)

            resp = self.success_stories_mail(date)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.acceptance_count(), count + 1)


#
# class AcceptanceCrud(AcceptanceTest):
#
#     pass


# class AcceptanceTestFromMail(AcceptanceTest):
#     """
#     item = {
#         fact_count: 1
#         good_id: 96
#         id: 44
#     }
#     """
#
#     def testAcceptenceFromMail(self):
#         with self.application.app_context():
#             self.invoice_()
#             response = self.acceptance_suite.invoice_items(self.invoice_id)
#             self.assertEqual(response.status_code, 200)
#
#             items = self._deserialize(response.data)
#             self.assertEqual(len(items['items']), 41)
#
#             items = [{'good_id': x['good_id'], 'id': x['id'], 'fact_count': num} for num, x in enumerate(items['items'][:10])]
#             count_pointitems = len(filter(lambda x: x['fact_count'], items))
#
#             for item in InvoiceItem.query.filter(
#                             InvoiceItem.invoice_id == self.invoice_id):
#                 self.assertIsNone(item.fact_count)
#
#             self.assertEqual(PointSaleItem.query.filter(
#                 PointSaleItem.pointsale_id == self.pointsale_id).count(), 0)
#             self.assertEqual(PointSaleItem.query.count(), 0)
#
#             response = self.acceptance_suite.acceptance_from_mail(
#                 self.invoice_id, self.pointsale_id, date=date.today(), items=items)
#             self.assertEqual(response.status_code, 200)
#
#             self.assertEqual(PointSaleItem.query.filter(
#                 PointSaleItem.pointsale_id == self.pointsale_id).count(), count_pointitems)
#             self.assertEqual(PointSaleItem.query.count(), count_pointitems)
#
#             for item in items:
#                 self.assertEqual(InvoiceItem.query.get(item['id']).fact_count, item['fact_count'] if item['fact_count'] else None)
#
#
# class AcceptanceTestCustom(AcceptanceTest):
#     """
#     item = {
#         good_id: 48
#         price_gross: "21"
#         price_post: "15"
#         price_retail: "24"
#     }
#     """
#
#     def testAcceptanceCustom(self):
#         with self.application.app_context():
#             PRICE_GROSS_1 = 5.5
#             PRICE_RETAIL_1 = 8.0
#             COUNT_1 = 5
#
#             PRICE_GROSS_2 = 7.9
#             PRICE_RETAIL_2 = 12.0
#             COUNT_2 = 15
#
#             PRICE_CHANGE_GROSS_2 = PRICE_GROSS_2 + 1
#             PRICE_CHANGE_RETAIL_2 = PRICE_RETAIL_2 + 1.5
#
#             PRICE_POST_1 = 3.8
#             PRICE_POST_2 = 7.0
#
#             self.good_id = self.application_suite.good(u"ЛТД", 5, 105, PRICE_RETAIL_1, PRICE_GROSS_1)
#             self.good_2_id = self.application_suite.good(u"Вечерние Челны", 22, 607, PRICE_RETAIL_2, PRICE_GROSS_2)
#             self.assertEqual(Price.query.count(), 2)
#             items = [
#                 {"good_id": self.good_id, "price_gross": PRICE_GROSS_1, "price_retail": PRICE_RETAIL_1, "price_post": PRICE_POST_1, "count_invoice": COUNT_1},
#                 {"good_id": self.good_2_id, "price_gross": PRICE_CHANGE_GROSS_2, "price_retail": PRICE_CHANGE_RETAIL_2, "price_post": PRICE_POST_2, "count_invoice": COUNT_2}
#             ]
#             response = self.acceptance_suite.acceptance_custom(
#                 self.pointsale_id, self.test_provider_id, date.today(), items)
#             self.assertEqual(response.status_code, 200)
#             data = self._deserialize(response.data)
#             invoice_id = data['data']['id']
#
#             good_1 = Good.query.get(self.good_id)
#             good_2 = Good.query.get(self.good_2_id)
#             invoice = Invoice.query.get(invoice_id)
#
#             self.assertEqual(Price.query.count(), 4)
#
#             self.assertEqual(PriceParish.query.filter(
#                 PriceParish.commodity_id == good_1.commodity_id,
#             ).count(), 1)
#
#             self.assertEqual(PriceParish.query.filter(
#                 PriceParish.commodity_id == good_2.commodity_id,
#             ).count(), 1)
#
#             self.assertEqual(float(good_1.price.price_gross), PRICE_GROSS_1)
#             self.assertEqual(float(good_1.price.price_retail), PRICE_RETAIL_1)
#             self.assertEqual(float(good_2.price.price_gross), PRICE_CHANGE_GROSS_2)
#             self.assertEqual(float(good_2.price.price_retail), PRICE_CHANGE_RETAIL_2)
#
#             invitem_1 = InvoiceItem.query.filter(
#                 InvoiceItem.invoice_id == invoice_id,
#                 InvoiceItem.good_id == self.good_id
#             ).first()
#             invitem_2 = InvoiceItem.query.filter(
#                 InvoiceItem.invoice_id == invoice_id,
#                 InvoiceItem.good_id == self.good_2_id
#             ).first()
#             self.assertEqual(invitem_1.fact_count, COUNT_1)
#             self.assertEqual(invitem_2.fact_count, COUNT_2)
#             self.assertEqual(float(invitem_1.price_with_NDS), PRICE_POST_1)
#             self.assertEqual(float(invitem_2.price_with_NDS), PRICE_POST_2)
#
#             pointsaleitem_1 = PointSaleItem.query.filter(
#                 PointSaleItem.good_id == self.good_id
#             ).first()
#             pointsaleitem_2 = PointSaleItem.query.filter(
#                 PointSaleItem.good_id == self.good_2_id
#             ).first()
#
#             self.assertEqual(pointsaleitem_1.count, COUNT_1)
#             self.assertEqual(pointsaleitem_2.count, COUNT_2)