# coding: utf-8

from flask.ext.restful import fields

from adminbuy.resources.core import BaseCanoniseResource

from .models import Commodity

__author__ = 'StasEvseev'


class CommodityCanonResource(BaseCanoniseResource):
    model = Commodity

    multif = {'filter_field': ('name', 'thematic')}

    attr_json = {
        'id': fields.Integer,
        'name': fields.String,
        'thematic': fields.String,
        'numeric': fields.Boolean,
        'num': fields.String
    }

    def pre_save(self, obj, data):
        if obj.id is None:
            if Commodity.query.filter(
                Commodity.name == obj.name
            ).count() > 0:
                raise CommodityCanonResource.CanonException(
                    u"Наименование номенклатуры должно быть уникальным."
                )
        else:
            if Commodity.query.filter(
                Commodity.name == obj.name,
                Commodity.id != obj.id
            ).count() > 0:
                raise CommodityCanonResource.CanonException(
                    u"Наименование номенклатуры должно быть уникальным."
                )
        return super(CommodityCanonResource, self).pre_save(obj, data)
