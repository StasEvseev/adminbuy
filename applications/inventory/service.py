# coding: utf-8

from applications.inventory.constant import (COUNT_AFTER_ATTR, GOOD_ATTR,
                                             GOOD_ID_ATTR, COUNT_BEFORE_ATTR)
from applications.inventory.models import (Inventory, InventoryItems,
                                           VALIDATED, DRAFT, StatusType)
from db import db
from log import debug
from services.core import BaseSQLAlchemyModelService


class InventoryService(BaseSQLAlchemyModelService):
    model = Inventory

    class InventoryServiceException(
        BaseSQLAlchemyModelService.ServiceException):
        pass

    @classmethod
    def exists_point(cls, location_id, id):
        """
        Проверяем, были ли инвентаризации в точке, помимо этой.
        """
        return cls.model.query.filter(
            cls.model.location_id == location_id,
            cls.model.id != id).count() > 0

    @classmethod
    def initial_inventory(cls, obj):
        """
        Инициализация ревизии. Если вдруг ревизия не первая, то нужно заполнить
        позиции ревизии пунктами из точки.
        """
        from applications.point_sale.service import PointSaleService
        try:
            location_id = obj.location_id
            if location_id:
                items = PointSaleService.items_pointsale(location_id)
                for item in items:
                    rev_item = cls.create_item(
                        obj.id, item.good_id, item.count, item.count)
                    db.session.add(rev_item)
        except Exception as exc:
            raise InventoryService.InventoryServiceException(unicode(exc))

    @classmethod
    def status(cls, inv, status):
        debug(u"Смена статуса `инвентаризации` %s с %s на %s" % (
            inv.id, inv.status, StatusType[status]))
        inv.status = status
        if status == VALIDATED:
            cls.sync_to_point(inv)

    @classmethod
    def create_item(cls, inventory_id, good_id, count_before,
                    count_after=None):
        return InventoryItems(inventory_id=inventory_id, good_id=good_id,
                              count_before=count_before,
                              count_after=count_after)

    @classmethod
    def sync_to_point(cls, obj):
        from applications.point_sale.service import PointSaleService
        try:
            location_id = obj.location_id
            exc_items = []
            if location_id:
                for item in obj.items:
                    pointitem = PointSaleService.sync_good(
                        location_id, item.good_id, item.count_after)
                    exc_items.append(pointitem.id)
            PointSaleService.none_count(location_id, exc_items)
        except Exception as exc:
            raise InventoryService.InventoryServiceException(unicode(exc))

    @classmethod
    def sync_from_json(cls, obj, json):
        """
        Сохранение позиций инвентаризации.
        """
        from applications.good.service import GoodService
        if obj.status not in [VALIDATED, DRAFT]:
            debug(u"Удаление связанных записей в инвентаризации (%s)" % obj.id)
            obj.items.delete()
            debug(u"Старт: Заполнение новых записей в инвентаризацию "
                  u"(%s)" % obj.id)
            for item in json:
                if COUNT_AFTER_ATTR not in item:
                    good = GoodService.get_good(item[GOOD_ATTR][GOOD_ID_ATTR])
                    raise InventoryService.InventoryServiceException(
                        u"Товар %s без количества после инвентаризации, "
                        u"не может быть сохранен в (%s)." % (
                            good.full_name, obj))
                in_item = cls.create_item(
                    obj.id, item[GOOD_ATTR][GOOD_ID_ATTR],
                    (item[COUNT_BEFORE_ATTR]
                     if COUNT_BEFORE_ATTR in item and item[COUNT_BEFORE_ATTR]
                     else 0),
                    item[COUNT_AFTER_ATTR])
                db.session.add(in_item)
            debug(u"Конец: Заполнение новых записей в инвентаризацию "
                  u"(%s)" % obj.id)
        else:
            debug(u"В статусе %s и %s позиции в инвентаризацию (%s) не "
                  u"сохраняются." % (VALIDATED, DRAFT, obj.id))
