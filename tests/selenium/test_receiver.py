#coding: utf-8
from applications.receiver.view import ReceiverAngularView
from all.selenium.test_common_ui import CommonTestUi


class GoodTest(CommonTestUi):
    VIEWS = ReceiverAngularView

    def testReceiverCRUD(self):
        self._test_crud()