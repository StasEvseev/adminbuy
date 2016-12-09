#coding: utf-8

__author__ = 'StasEvseev'

from applications.seller.model import Seller

from adminbuy.app import db
from tests.helpers.suits import BaseSuite


class SellerSuite(BaseSuite):

    def create_test_seller(self):
        # with self.application.app_context():
        seller = Seller(fname='fname', lname="lname", pname="pname", address='address', passport="passport")
        db.session.add(seller)
        db.session.commit()
        return seller.id