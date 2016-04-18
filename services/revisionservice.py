# coding: utf-8

from db import db

from models.revision import Revision, RevisionItem

from services.core import BaseSQLAlchemyModelService


class RevisionService(BaseSQLAlchemyModelService):
    model = Revision

    class RevisionServiceException(
            BaseSQLAlchemyModelService.ServiceException):
        pass

    @classmethod
    def exists_point(cls, pointsale_id, id):
        return cls.model.query.filter(
            Revision.pointsale_id == pointsale_id,
            Revision.id != id).count() > 0

    @classmethod
    def initial_revision(cls, obj):
        """
        Инициализация ревизии. Если вдруг ревизия не первая, то нужно заполнить
        позиции ревизии пунктами из точки.
        """
        from applications.point_sale.service import PointSaleService
        try:
            pointsale_id = obj.pointsale_id
            if pointsale_id and cls.exists_point(pointsale_id, obj.id):
                items = PointSaleService.items_pointsale(pointsale_id)
                for item in items:
                    rev_item = RevisionService.create_item(
                        obj.id, item.good_id, item.count)
                    db.session.add(rev_item)
        except Exception as exc:
            raise RevisionService.RevisionServiceException(unicode(exc))

    @classmethod
    def sync_to_point(cls, obj):
        from applications.point_sale.service import PointSaleService
        try:
            pointsale_id = obj.pointsale_id
            exc_items = []
            if pointsale_id:
                for item in obj.items:
                    pointitem = PointSaleService.sync_good(
                        pointsale_id, item.good_id, item.count_after)
                    exc_items.append(pointitem.id)
            PointSaleService.none_count(pointsale_id, exc_items)
        except Exception as exc:
            raise RevisionService.RevisionServiceException(unicode(exc))

    @classmethod
    def create_item(cls, revision_id, good_id, count):
        return RevisionItem(
            revision_id=revision_id, good_id=good_id, count_before=count)
