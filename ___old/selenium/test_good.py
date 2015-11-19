#coding: utf-8\n__author__ = 'StasEvseev'
from ___old.selenium.test_common_ui import CommonTestUi
from applications.good.views import GoodViewAngular


class GoodTest(CommonTestUi):
    VIEWS = GoodViewAngular

    def testGoodCRUD(self):
        self._test_crud()