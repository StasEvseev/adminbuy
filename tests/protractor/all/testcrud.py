# coding: utf-8
__author__ = 'StasEvseev'

import os

from tests.protractor.test import BaseProtractorTestCase


class TestProtractorCrud(BaseProtractorTestCase):

    def set_up(self):
        self.application.create_superuser()

    def test(self):
        self.run_test(os.path.join("testcrud", "conf.js"))