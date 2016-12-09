# coding: utf-8

from adminbuy.applications.commodity.models import Commodity

from ...helpers.suits.commodity import CommodityTestSuite
from ...helpers.suits.good import GoodTestSuite


__author__ = 'StasEvseev'


class ApplicationSuite(object):

    def __init__(self, client, application):
        self.client = client
        self.application = application

        self.commodity_suite = CommodityTestSuite(self.client, self.application)
        self.good_suite = GoodTestSuite(self.client, self.application)

    def good(self, name, number_l, number_g, price_retail, price_gross):
        # if number_l is None and number_g is None:
        #     numeric = False
        numeric = False if number_l is None and number_g is None else True
        with self.application.app_context():
            com = Commodity.query.filter(Commodity.name == name)
            if com.count() > 0:
                com_id = com[0].id
            else:
                com_id = self.commodity_suite.create_commodity(name, numeric, "")["id"]
        res = self.good_suite.create_good(com_id, number_l, number_g, price_retail, price_gross)
        good_id = res["id"]

        return good_id

    def acceptance_mail(self, file_name, pointsale_id, date):

        pass
