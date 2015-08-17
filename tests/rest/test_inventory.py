#coding: utf-8
from applications.inventory.constant import COUNT_AFTER_ATTR, GOOD_ATTR, GOOD_ID_ATTR
from applications.inventory.models import InventoryItems, IN_PROG, VALIDATED
from applications.point_sale.models import PointSaleItem

from all import BaseTestCase
from all.helpers import Generator
from all.helpers.suits.application import ApplicationSuite
from all.helpers.suits.inventory import InventorySuite
from all.helpers.suits.pointsale import PointSaleSuite


class InventoryTest(BaseTestCase):

    def set_up(self):
        self.pointsale_suite = PointSaleSuite(self.client, self.application)
        self.inventory_suite = InventorySuite(self.client, self.application)
        self.application_suite = ApplicationSuite(self.client, self.application)

        with self.application.app_context():
            self.number_1 = Generator.generate_int()
            self.number_2 = Generator.generate_int()
            self.pointsale_id = self.pointsale_suite.create_test_pointsale("", "").id
            self.good_id_1 = self.application_suite.good(u"ЛТД", '1', '101', 8, 5.5)
            self.good_id_2 = self.application_suite.good(u"Вечерние Челны", '4', '402', 12.0, 9.7)
            self.good_id_3 = self.application_suite.good(u"WinX", '25', '107', 147.0, 123.0)
            self.good_id_4 = self.application_suite.good(u"Трансформеры", '4', '7', 120.0, 97.0)

    def get_pointsaleitem(self, pointsale_id, good_id):
        return PointSaleItem.query.filter(
            PointSaleItem.pointsale_id == pointsale_id,
            PointSaleItem.good_id == good_id).one()

    def get_inventoryitem(self, inventory_id, good_id):
        return InventoryItems.query.filter(
            InventoryItems.inventory_id == inventory_id,
            InventoryItems.good_id == good_id).one()

    def test_(self):
        #Кол-ва товара в накладную
        count_after_1 = 100
        count_after_2 = 67
        with self.application.app_context():
            response = self.inventory_suite.create_inventory(self.pointsale_id, self.number_1)

            self.assertEqual(response.status_code, 200)
            data = self._deserialize(response.data)
            inventory_id_1 = data['id']

            self.assertEqual(InventoryItems.query.filter(
                InventoryItems.inventory_id == inventory_id_1
            ).count(), 0)

            response = self.inventory_suite.inventory_status(inventory_id_1, IN_PROG)
            self.assertEqual(response.status_code, 200)

            self.assertEqual(InventoryItems.query.filter(
                InventoryItems.inventory_id == inventory_id_1
            ).count(), 0)

            items = [
                {COUNT_AFTER_ATTR: count_after_1, GOOD_ATTR: {GOOD_ID_ATTR: self.good_id_1}},
                {COUNT_AFTER_ATTR: count_after_2, GOOD_ATTR: {GOOD_ID_ATTR: self.good_id_2}}
            ]

            response = self.inventory_suite.update_inventory(inventory_id_1, items=items)
            self.assertEqual(response.status_code, 200)

            self.assertEqual(InventoryItems.query.filter(
                InventoryItems.inventory_id == inventory_id_1
            ).count(), 2)
            self.assertEqual(PointSaleItem.query.filter(
                PointSaleItem.pointsale_id == self.pointsale_id
            ).count(), 0)

            response = self.inventory_suite.inventory_status(inventory_id_1, VALIDATED)
            self.assertEqual(response.status_code, 200)

            self.assertEqual(InventoryItems.query.filter(
                InventoryItems.inventory_id == inventory_id_1
            ).count(), 2)
            self.assertEqual(PointSaleItem.query.filter(
                PointSaleItem.pointsale_id == self.pointsale_id
            ).count(), 2)
            pointsaleitem_1 = self.get_pointsaleitem(self.pointsale_id, self.good_id_1)
            pointsaleitem_2 = self.get_pointsaleitem(self.pointsale_id, self.good_id_2)
            self.assertEqual(pointsaleitem_1.count, count_after_1)
            self.assertEqual(pointsaleitem_2.count, count_after_2)


            response = self.inventory_suite.create_inventory(self.pointsale_id, self.number_2)
            self.assertEqual(response.status_code, 200)
            data = self._deserialize(response.data)
            inventory_id_2 = data['id']

            self.assertEqual(InventoryItems.query.filter(
                InventoryItems.inventory_id == inventory_id_2
            ).count(), 2)

            inventory_item_1 = self.get_inventoryitem(inventory_id_2, self.good_id_1)
            inventory_item_2 = self.get_inventoryitem(inventory_id_2, self.good_id_2)

            self.assertEqual(inventory_item_1.count_before, count_after_1)
            self.assertEqual(inventory_item_2.count_before, count_after_2)

            self.assertEqual(inventory_item_1.count_after, count_after_1)
            self.assertEqual(inventory_item_2.count_after, count_after_2)