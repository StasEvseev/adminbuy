# coding: utf-8
from models.sync import WorkDay
from services.core import BaseSQLAlchemyModelService

__author__ = 'StasEvseev'


class SyncService(BaseSQLAlchemyModelService):
    model = WorkDay

    @classmethod
    def get_or_create(cls, user_id, datetime_start):
        query = cls.model.query.filter(cls.model.user_id==user_id, cls.model.datetime_start==datetime_start)
        if query.count() > 0:
            return query.first()
        inst = cls.model()
        inst.user_id = user_id
        inst.datetime_start = datetime_start
        return inst