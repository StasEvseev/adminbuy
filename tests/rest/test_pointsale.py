#coding: utf-8

__author__ = 'StasEvseev'

from tests import BaseTestCase
from tests.helpers.suits.pointsale import PointSaleSuite


class PointsaleTest(BaseTestCase):

    def set_up(self):
        self.pointsale_suite = PointSaleSuite(self.client, self.application)

    def testUniqMainPointsale(self):
        response = self.pointsale_suite.create_pointsale_rest(name=u"Точка1", address=u"Адрес1", is_central=True)
        self.assertEqual(response.status_code, 200)
        id = self._deserialize(response.data)['id']

        response = self.pointsale_suite.create_pointsale_rest(name=u"Точка2", address=u"Адрес2", is_central=True)
        self.assertEqual(response.status_code, 400)
        response = self.pointsale_suite.create_pointsale_rest(name=u"Точка2", address=u"Адрес2", is_central=False)
        self.assertEqual(response.status_code, 200)
        id_2 = self._deserialize(response.data)['id']
        response = self.pointsale_suite.update_pointsale_rest(id_2, is_central=True)
        self.assertEqual(response.status_code, 400)

        response = self.pointsale_suite.update_pointsale_rest(id, is_central=False)
        self.assertEqual(response.status_code, 200)