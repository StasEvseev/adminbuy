# coding: utf-8

__author__ = 'StasEvseev'


class BaseService(object):
    class ServiceException(Exception):
        pass


class BaseSQLAlchemyModelService(BaseService):
    model = None

    @classmethod
    def get_by_id(cls, id):
        return cls.model.query.get(id)

    @classmethod
    def create_instance(cls, **kwargs):
        return cls.model(**kwargs)

    @classmethod
    def exists_exclude_id(cls, id):
        return cls.model.query.filter(
            cls.model.id != id).count() > 0
