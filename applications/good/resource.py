#coding: utf-8
from flask.ext.restful import fields, abort

from applications.good.model import Good
from applications.good.service import GoodService, GoodServiceException

from resources.core import BaseCanoniseResource


class GoodResourceCanon(BaseCanoniseResource):
    model = Good

    class GoodResourceException(BaseCanoniseResource.CanonException):
        pass

    multif = {'filter_field': ('full_name', 'number_local', 'number_global')}

    attr_json = {
        'id': fields.Integer,
        'full_name': fields.String,
        'full_name_with_price': fields.String,
        'commodity_id': fields.Integer,
        'commodity': fields.Nested({
            'id': fields.Integer,
            'name': fields.String,
            'numeric': fields.Boolean,
        }),
        'number_local': fields.String,
        'number_global': fields.String,
        'barcode': fields.String,
        'price_id': fields.Integer(default=None),
        'price.price_gross': fields.String(attribute="price.price_gross"),
        'price.price_retail': fields.String(attribute='price.price_retail')
    }

    def pre_save(self, obj, data):
        from applications.commodity.service import CommodityService
        obj.number_local = str(obj.number_local) if obj.number_local else None
        obj.number_global = str(obj.number_global) if obj.number_global else None
        if obj.commodity_id is None:
            raise GoodResourceCanon.GoodResourceException(u"Нельзя сохранить товар без номенклатуры.")
        commodity = CommodityService.get_by_id(obj.commodity_id)
        try:
            res, good = GoodService.get_or_create_commodity_numbers(
                obj.commodity_id, obj.number_local, obj.number_global, obj.id)
        except GoodServiceException as exc:
            raise GoodResourceCanon.GoodResourceException(unicode(exc))

        if res is False:
            good.commodity = commodity
            price_id = data.get('price_id')
            if price_id:
                good.price_id = price_id
            if not data.get('full_name'):
                full_name = GoodService.full_name(good)
            else:
                full_name = obj.full_name
            good.full_name = full_name
            good.barcode = data.get('barcode')
        if res is True:
            if commodity.numeric:
                message = u"В системе уже есть товар с наименованием %s и №%s(%s)" % (commodity.name, obj.number_local, obj.number_global)
            else:
                message = u"В системе уже есть безномерной товар с наименованием %s" % commodity.name
            raise GoodResourceCanon.GoodResourceException(message)
        good = super(GoodResourceCanon, self).pre_save(good, data)
        return good

    def get(self, id):
        try:
            good = GoodService.get_good(id)
        except GoodServiceException as err:
            abort(404, message=unicode(err))
        return good


ATTR_ITEM = {
    'id': fields.Integer,
    'full_name': fields.String,
    'commodity_id': fields.Integer,
    'number_local': fields.String,
    'number_global': fields.String
}


def good_from_dict(data):
    """
    извлекает данные для Продукта из словаря
    """
    commodity_id = data.get('commodity_id')
    number_local = data.get('number_local')
    number_global = data.get('number_global')
    price_id = data.get('price_id')
    full_name = data.get('full_name')
    barcode = data.get('barcode')
    return commodity_id, number_local, number_global, price_id, full_name, barcode