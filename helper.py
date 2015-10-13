#coding: utf-8

__author__ = 'StasEvseev'

from flask.ext.sqlalchemy import _BoundDeclarativeMeta


def get_relation_model(obj, name):
    relation_model = obj._sa_class_manager[name].property.argument
    if isinstance(relation_model, _BoundDeclarativeMeta):
        return relation_model
    else:
        return relation_model._dict[relation_model.arg].cls