# coding: utf-8

from flask.ext.restful import fields, marshal_with

from resources.core import (BaseCanoniseResource, BaseInnerCanon, ExtraMixin,
                            BasePrintResource, BaseStatusResource)

from applications.inventory.constant import (COUNT_AFTER_ATTR, GOOD_ATTR,
                                             GOOD_ID_ATTR, COUNT_BEFORE_ATTR)
from applications.inventory.models import Inventory, InventoryItems, VALIDATED
from applications.inventory.service import InventoryService

from log import warning


attr = {
    'id': fields.Integer,
    'number': fields.String,
    'datetimenew': fields.DateTime(dt_format='iso8601'),
    'location_id': fields.Integer,
    'location_name': fields.String(attribute="location.name"),
    'status': fields.Integer(attribute="status.code"),
    'status_str': fields.String(attribute="status.value"),
}


ATTR_ITEMS = {
    'id': fields.Integer,
    GOOD_ATTR: fields.Nested({
        GOOD_ID_ATTR: fields.Integer,
        'full_name_with_price': fields.String,
        'full_name': fields.String,
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
    }),
    'good_id': fields.Integer,
    'good.full_name': fields.String,
    COUNT_BEFORE_ATTR: fields.Integer,
    COUNT_AFTER_ATTR: fields.Integer
}


class InventoryItemCanon(BaseCanoniseResource):
    model = InventoryItems

    attr_json = ATTR_ITEMS


class InventoryItemInnerCanon(BaseInnerCanon):
    inner_model = Inventory
    model = InventoryItems

    attr_json = ATTR_ITEMS

    default_sort = 'asc', 'id'


class ExtraMixinItemsInventory(ExtraMixin):
    def post_save(self, obj, data, create_new=True):
        super(ExtraMixinItemsInventory, self).post_save(obj, data, create_new)
        if 'items' in data:
            try:
                InventoryService.sync_from_json(obj, data['items'])
            except InventoryService.InventoryServiceException as exc:
                raise BaseCanoniseResource.CanonException(unicode(exc))


class InventoryCanon(ExtraMixinItemsInventory, BaseCanoniseResource):
    model = Inventory

    attr_json = attr

    def post_save(self, obj, data, create_new=False):
        super(InventoryCanon, self).post_save(obj, data, create_new)

        if create_new:
            InventoryService.initial_inventory(obj)

    def pre_delete(self, obj):
        if obj.status == VALIDATED:
            warning(u"Попытка удалить инвентаризацию в завершенном статусе "
                    u"(%s)." % obj.id)
            raise BaseCanoniseResource.CanonException(
                u"Нельзя удалять инвентаризацию, в завершенном статусе.")


class InventoryStatusResource(BaseStatusResource):
    service = InventoryService

    @marshal_with(attr)
    def post(self, id):
        return self._action(id)


class InventoryPrint(BasePrintResource):
    TEMPLATE = "print_inventory.xls"

    def handle(self, pi, id):
        from applications.good.service import GoodService
        inventory = InventoryService.get_by_id(id)

        su = sum(map(lambda it: GoodService.get_price(
            it.good_id).price_retail * it.count_after, inventory.items))

        pi.set_cells(0, 0, [('number', 2)])
        pi.set_cells(0, 2, ['a', 'date', 'c', 'c', 'c', 'sum'])
        pi.set_cells(0, 3, ['a', 'pointsale'])
        pi.set_cells(0, 6, [('name', 5), 'price', 'a', 'count', 'b', 'c', 'd'])

        pi.write(0, 0, 0, [{'number': inventory.number}])
        pi.write(0, 2, 1, [{'date': inventory.datetimenew.strftime(
            "%d.%m.%Y - %H:%M:%S"), 'sum': su}])
        pi.write(0, 3, 0, [{'pointsale': inventory.location.name}])

        items = [
            {'name': it.good.full_name, 'count': it.count_after or "",
             'price': GoodService.get_price(it.good_id).price_retail,
             'a': '',
             'b': '',
             'c': '',
             'd': ''} for it in inventory.items]
        pi.write(0, 6, 2, items)
