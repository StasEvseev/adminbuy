#coding: utf-8
from applications.point_sale.models import PointSaleItem
from applications.waybill.constant import GOOD_ATTR, COUNT_ATTR

from models.invoice import Invoice

from tests import BaseTestCase
from tests.helpers import Generator
from tests.helpers.suits.application import ApplicationSuite
from tests.helpers.suits.commodity import CommodityTestSuite
from tests.helpers.suits.good import GoodTestSuite
from tests.helpers.suits.invoice import MailInvoiceTestSuite
from tests.helpers.suits.pointsale import PointSaleSuite
from tests.helpers.suits.providersuit import ProviderTestSuite
from tests.helpers.suits.receiver import ReceiverSuite
from tests.helpers.suits.waybill import WayBillTestSuite
from applications.waybill.models import WayBill, RETAIL, GROSS, POINTSALE, RECEIVER, IN_PROG, IN_DELIVERY, FINISH


class WayBillTest(BaseTestCase):
    def set_up(self):
        self.receiver_suite = ReceiverSuite(self.client, self.application)
        self.pointsale_suite = PointSaleSuite(self.client, self.application)
        self.waybill_suite = WayBillTestSuite(self.client, self.application)

    def init_relation_models(self):
        self.receiver = self.receiver_suite.create_test_receiver()
        self.receiver_id = self.receiver.id
        self.point_1 = self.pointsale_suite.create_test_pointsale(
            name=u"ШШК", address=u"наб. Челны", is_central=True)
        self.point_1_id = self.point_1.id
        self.point_2 = self.pointsale_suite.create_test_pointsale(
            name=u"Одиссей", address=u"Наб. Челны, ул. Беляева, 75")
        self.point_2_id = self.point_2.id
        self.point_3 = self.pointsale_suite.create_test_pointsale(
            name=u"Форт Диалог", address=u"Наб. Челны, Московский пр., 15")
        self.point_3_id = self.point_3.id

        self.application_suite = ApplicationSuite(self.client, self.application)
        self.good_id = self.application_suite.good(u"XXL", '77', '114', 105.0, 86.0)
        self.good_2_id = self.application_suite.good(u"Машинка", None, None, 24.0, 21.0)
        self.good_3_id = self.application_suite.good(u"ЗОЖ", '4', '105', None, 9.5)
        self.good_4_id = self.application_suite.good(u"Мельница", None, None, 15.0, None)

        self.COUNT_GOOD_1 = 10
        self.COUNT_GOOD_4 = 5
        self.COUNT_GOOD_2 = 7

        self.items = [
            {GOOD_ATTR: self.good_id, COUNT_ATTR: self.COUNT_GOOD_1},
            {GOOD_ATTR: self.good_4_id, COUNT_ATTR: self.COUNT_GOOD_4}]

        self.items_2 = [{GOOD_ATTR: self.good_2_id, COUNT_ATTR: self.COUNT_GOOD_2}]


class WayBillTestCRUD(WayBillTest):

    def crush(self):
        count = WayBill.query.count()
        #TEST CRASH
        #Создаем накладную без получателя и точки
        response = self.waybill_suite.create_waybill(
            date=unicode(self.date), receiver_id=None, pointsale_id=None, type=RETAIL, invoice_id=None,
            pointsale_from_id=None, items=[], typeRec=POINTSALE
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(WayBill.query.count(), count)

        #Создаем накладную без точки отправителя
        response = self.waybill_suite.create_waybill(
            date=unicode(self.date), receiver_id=self.receiver_id, pointsale_id=None, type=RETAIL, invoice_id=None,
            pointsale_from_id=None, items=[], typeRec=POINTSALE)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(WayBill.query.count(), count)

        #Создаем накладную неизвестного типа
        response = self.waybill_suite.create_waybill(
            date=unicode(self.date), receiver_id=self.receiver_id, type=3, invoice_id=None,
            pointsale_from_id=self.point_1_id, items=[], typeRec=RECEIVER
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(WayBill.query.count(), count)

        #Создаем накладную с циклической ссылкой(откуда уходит товар, туда и приходит)
        response = self.waybill_suite.create_waybill(
            date=unicode(self.date), pointsale_id=self.point_1_id, type=RETAIL, invoice_id=None,
            pointsale_from_id=self.point_1_id, items=[], typeRec=POINTSALE
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(WayBill.query.count(), count)

        #Создание розничной накладной с товаром в котором только оптовая цена
        response = self.waybill_suite.create_waybill(
            date=unicode(self.date), pointsale_id=self.point_1_id, type=RETAIL, invoice_id=None,
            pointsale_from_id=self.point_2_id, items=[{
                GOOD_ATTR: self.good_3_id,
                COUNT_ATTR: 15
            }], typeRec=POINTSALE)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(WayBill.query.count(), count)

        #Создание оптовой накладной с товаром в котором только розничная цена
        response = self.waybill_suite.create_waybill(
            date=unicode(self.date), pointsale_id=self.point_1_id, type=GROSS, invoice_id=None,
            pointsale_from_id=self.point_2_id, items=[{
                GOOD_ATTR: self.good_4_id,
                COUNT_ATTR: 15
            }], typeRec=POINTSALE
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(WayBill.query.count(), count)

    def testWaybillFromOnePointToOtherPoint(self):
        with self.application.app_context():
            self.init_relation_models()

            self.date = Generator.generate_date()
            self.date_2 = Generator.generate_date()
            self.items = [
                {GOOD_ATTR: self.good_id, COUNT_ATTR: 10},
                {GOOD_ATTR: self.good_4_id, COUNT_ATTR: 5}]
            self.items_2 = [{GOOD_ATTR: self.good_2_id, COUNT_ATTR: 7}]
            self.crush()

            response = self.waybill_suite.create_waybill(
                date=unicode(self.date), pointsale_id=self.point_2_id, type=RETAIL, receiver_id=self.receiver_id,
                invoice_id=None, pointsale_from_id=self.point_1_id, items=self.items, typeRec=POINTSALE)

            self.assertEqual(response.status_code, 200)
            data = self._deserialize(response.data)

            self.assertEqual(WayBill.query.count(), 1)
            waybill = WayBill.query.first()

            self.assertEqual(waybill.pointsale_id, self.point_2_id)
            self.assertEqual(waybill.pointsale_from_id, self.point_1_id)
            self.assertEqual(waybill.type, RETAIL)
            self.assertEqual(waybill.date, self.date)
            self.assertEqual(waybill.items.count(), len(self.items))
            self.assertIsNone(waybill.receiver)

            response = self.waybill_suite.get_waybill(waybill.id)
            self.assertEqual(response.status_code, 200)

            response = self.waybill_suite.update_waybill(waybill.id, date=unicode(self.date_2), items=self.items_2)
            self.assertEqual(response.status_code, 200)

            waybill = WayBill.query.get(waybill.id)
            self.assertEqual(waybill.date, self.date_2)
            self.assertEqual(waybill.items.count(), len(self.items_2))


class WayBillStatus(WayBillTest):

    # def set_up(self):
        # self.receiver_suite = ReceiverSuite(self.client, self.application)
        # self.pointsale_suite = PointSaleSuite(self.client, self.application)
        # self.waybill_suite = WayBillTestSuite(self.client, self.application)

    def testWayBillStatus(self):
        with self.application.app_context():
            self.init_relation_models()

            self.date = Generator.generate_date()

            response = self.waybill_suite.create_waybill(
                date=unicode(self.date), pointsale_id=self.point_2_id, type=RETAIL,
                invoice_id=None, pointsale_from_id=self.point_1_id, items=self.items, typeRec=POINTSALE)
            self.assertEqual(response.status_code, 200)
            id = self._deserialize(response.data)['id']
            self.assertEqual(PointSaleItem.query.filter(
                PointSaleItem.pointsale_id == self.point_1_id
            ).count(), 0)
            self.assertEqual(PointSaleItem.query.filter(
                PointSaleItem.pointsale_id == self.point_2_id
            ).count(), 0)

            response = self.waybill_suite.update_status(id, IN_PROG)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(PointSaleItem.query.filter(
                PointSaleItem.pointsale_id == self.point_1_id
            ).count(), 0)
            self.assertEqual(PointSaleItem.query.filter(
                PointSaleItem.pointsale_id == self.point_2_id
            ).count(), 0)

            response = self.waybill_suite.update_status(id, IN_DELIVERY)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(PointSaleItem.query.filter(
                PointSaleItem.pointsale_id == self.point_1_id
            ).count(), 0)
            self.assertEqual(PointSaleItem.query.filter(
                PointSaleItem.pointsale_id == self.point_2_id
            ).count(), 0)

            response = self.waybill_suite.update_status(id, FINISH)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(PointSaleItem.query.filter(
                PointSaleItem.pointsale_id == self.point_1_id
            ).count(), 2)
            self.assertEqual(PointSaleItem.query.filter(
                PointSaleItem.pointsale_id == self.point_2_id
            ).count(), 2)

            pointsale_item_1 = PointSaleItem.query.filter(
                PointSaleItem.pointsale_id == self.point_1_id,
                PointSaleItem.good_id == self.good_id
            ).one()
            pointsale_item_2 = PointSaleItem.query.filter(
                PointSaleItem.pointsale_id == self.point_1_id,
                PointSaleItem.good_id == self.good_4_id
            ).one()

            self.assertEqual(pointsale_item_1.count, self.COUNT_GOOD_1 * -1)
            self.assertEqual(pointsale_item_2.count, self.COUNT_GOOD_4 * -1)

            pointsale_item_1 = PointSaleItem.query.filter(
                PointSaleItem.pointsale_id == self.point_2_id,
                PointSaleItem.good_id == self.good_id
            ).one()
            pointsale_item_2 = PointSaleItem.query.filter(
                PointSaleItem.pointsale_id == self.point_2_id,
                PointSaleItem.good_id == self.good_4_id
            ).one()

            self.assertEqual(pointsale_item_1.count, self.COUNT_GOOD_1)
            self.assertEqual(pointsale_item_2.count, self.COUNT_GOOD_4)