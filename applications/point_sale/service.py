#coding: utf-8

__author__ = 'StasEvseev'

from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound

from db import db
from applications.point_sale.models import PointSale, PointSaleItem


class PointSaleService(object):

    class PointSaleServiceException(Exception):
        pass

    @classmethod
    def point_save(cls, obj, name, address, is_central=False):
        if is_central is True and cls.has_central(obj.id):
            raise PointSaleService.PointSaleServiceException(u"Нельзя создавать более одной центральной точки.")
        obj.name = name
        obj.address = address
        obj.is_central = is_central
        db.session.add(obj)
        return obj

    @classmethod
    def get_central(cls):
        pointsl = PointSale.query.filter(PointSale.is_central==True)
        if pointsl.count() < 1:
            raise PointSaleService.PointSaleServiceException(u"В системе не заведено центральной точки.")
        if pointsl.count() > 1:
            raise PointSaleService.PointSaleServiceException(u"В системе не заведено больше одной центральной точки.")
        return pointsl.one()

    @classmethod
    def has_central(cls, exc_id=None):
        pointsl = PointSale.query.filter(PointSale.is_central == True)
        if exc_id:
            pointsl = pointsl.filter(PointSale.id != exc_id)
        return pointsl.count() > 0

    @classmethod
    def get_all(cls):
        return PointSale.query.all()

    @classmethod
    def get_all_exclude(cls, exclude_id):
        return PointSale.query.filter(PointSale.id != exclude_id)

    @classmethod
    def get_by_id(cls, id):
        return PointSale.query.get(id)

    @classmethod
    def get_or_create(cls, point_id, good_id):
        pointitem = cls.item_to_pointsale_good(point_id, good_id)
        if pointitem is None:
            pointitem = PointSaleItem()
            pointitem.pointsale_id = point_id
            pointitem.good_id = good_id
            pointitem.count = 0
            db.session.add(pointitem)
        return pointitem

    @classmethod
    def sync_good(cls, pointsale_id, good_id, count):
        item = cls.get_or_create(pointsale_id, good_id)
        item.count = count
        db.session.add(item)
        db.session.flush()
        return item

    @classmethod
    def sync_good_increment(cls, pointsale_id, good_id, count):
        item = cls.get_or_create(pointsale_id, good_id)
        item.count += count
        db.session.add(item)
        db.session.flush()
        return item

    @classmethod
    def item_to_pointsale_good(cls, pointsale_id, good_id):
        try:
            return PointSaleItem.query.filter(
                PointSaleItem.pointsale_id==pointsale_id,
                PointSaleItem.good_id==good_id).one()
        except NoResultFound:
            pass

    @classmethod
    def none_count(cls, point_id, excl_items=None):
        items = cls.items_pointsale(point_id, excl_items)
        for item in items:
            db.session.delete(item)

    @classmethod
    def items_pointsale(cls, point_id, excl_items=None):
        if excl_items:
            return PointSaleItem.query.filter(
                and_(PointSaleItem.pointsale_id==point_id,
                     PointSaleItem.id.notin_(excl_items)))
        else:
            return PointSaleItem.query.filter(
                PointSaleItem.pointsale_id==point_id)