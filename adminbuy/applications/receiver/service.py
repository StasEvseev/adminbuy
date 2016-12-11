# coding: utf-8

from adminbuy.services.core import BaseSQLAlchemyModelService

from .model import Receiver


__author__ = 'StasEvseev'


class ReceiverService(BaseSQLAlchemyModelService):
    model = Receiver

    @classmethod
    def get_all(cls):
        return Receiver.query.all()
