#coding: utf-8

__author__ = 'StasEvseev'

from applications.receiver.model import Receiver


class ReceiverService(object):

    @classmethod
    def get_all(cls):
        return Receiver.query.all()