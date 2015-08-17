#coding: utf-8
from app import db
from applications.receiver.model import Receiver

from all.helpers.suits import BaseSuite
# from models import db


class ReceiverSuite(BaseSuite):
    """
    Сьют для создания получателей.
    """

    def create_test_receiver(self):
        # with self.application.app_context():
        receiver = Receiver(fname=u"Фазлеев", lname=u"Рафик", pname=u"Назарович", address=u"Наб. Челны", passport="1223 987212")
        # db.session()
        db.session.add(receiver)
        db.session.commit()
        return receiver