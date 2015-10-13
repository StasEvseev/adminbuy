#coding: utf-8\n__author__ = 'StasEvseev'
from applications.good.views import GoodViewAngular
from tests.selenium.test_common_ui import CommonTestUi


class GoodTest(CommonTestUi):
    VIEWS = GoodViewAngular

    def testGoodCRUD(self):
        self._test_crud()