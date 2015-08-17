#coding: utf-8
from applications.receiver.model import Receiver


class ReceiverService(object):

    @classmethod
    def get_all(cls):
        return Receiver.query.all()