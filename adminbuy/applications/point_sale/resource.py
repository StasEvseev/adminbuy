# coding: utf-8

from flask import request
from flask.ext.restful import fields

from adminbuy.resources.core import BaseCanoniseResource, BaseInnerCanon

from .service import PointSaleService
from adminbuy.applications.point_sale.models import PointSale, PointSaleItem


__author__ = 'StasEvseev'


class PointSaleCanon(BaseCanoniseResource):
    model = PointSale

    attr_json = {
        'id': fields.Integer,
        'name': fields.String,
        'address': fields.String,
        'is_central': fields.Boolean
    }

    multif = {'filter_field': ("name", "address")}

    def filter_query(self, query, filter_field, filter_text, sort_field,
                     sort_course, page, count):
        try:
            exclude_points = request.args['exclude_point_id']
        except KeyError:
            pass
        else:
            query = query.filter(
                self.model.id != exclude_points
            )
        try:
            is_cent = request.args['is_central']
        except KeyError:
            pass
        else:
            query = query.filter(
                self.model.is_central == is_cent
            )

        return super(PointSaleCanon, self).filter_query(
            query, filter_field, filter_text, sort_field, sort_course, page,
            count)

    def pre_save(self, obj, data):
        try:
            point = PointSaleService.point_save(
                obj=obj, name=obj.name, address=obj.address,
                is_central=obj.is_central)
        except PointSaleService.PointSaleServiceException as exc:
            raise BaseCanoniseResource.CanonException(unicode(exc))
        return point


class PointSaleItemInnerCanon(BaseInnerCanon):
    inner_model = PointSale
    model = PointSaleItem

    multif = {"filter_field": ('good.full_name', )}

    default_sort = 'asc', 'id'

    attr_json = {
        'id': fields.Integer,
        'count': fields.Integer(attribute='count'),
        'good_id': fields.Integer(attribute='good.id'),
        'full_name': fields.String(attribute='good.full_name'),
        'price_retail': fields.String(attribute='good.price.price_retail'),
        'price_gross': fields.String(attribute='good.price.price_gross'),
        'good': fields.Nested({
            'id': fields.Integer,
            'full_name': fields.String,
            'price': fields.Nested({
                'price_retail': fields.Float,
                'price_gross': fields.Float})
        }),
    }
