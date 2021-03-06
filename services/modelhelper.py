# coding: utf-8

__author__ = 'StasEvseev'


class ModelService(object):
    """
    Модельный сервис. Всякие вспомогательные функции.
    """

    @classmethod
    def check_id(cls, id):
        """
        Проверяет, id не затерт ли.
        """
        return id not in [0, -1, None]
