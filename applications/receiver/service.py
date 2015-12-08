# coding: utf-8

from applications.receiver.model import Receiver
from services.core import BaseSQLAlchemyModelService

__author__ = 'StasEvseev'


class ReceiverService(BaseSQLAlchemyModelService):
    model = Receiver

    @classmethod
    def get_all(cls):
        return Receiver.query.all()
