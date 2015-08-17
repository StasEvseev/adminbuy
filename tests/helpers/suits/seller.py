#coding: utf-8
# from models import db
from app import db
from applications.seller.model import Seller
from all.helpers.suits import BaseSuite


class SellerSuite(BaseSuite):

    def create_test_seller(self):
        # with self.application.app_context():
        seller = Seller(fname='fname', lname="lname", pname="pname", address='address', passport="passport")
        db.session.add(seller)
        db.session.commit()
        return seller.id