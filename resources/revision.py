#coding: utf-8

__author__ = 'StasEvseev'

from flask.ext.restful import fields, abort
from log import error

from models.revision import Revision, RevisionItem
from db import db

from resources import Date
from resources.core import BaseCanoniseResource, BaseTokeniseResource

from services.helperserv import HelperService
from services.revisionservice import RevisionService


class RevisionApprove(BaseTokeniseResource):
    def post(self, id):
        try:
            revision = RevisionService.get_by_id(id)
            RevisionService.sync_to_point(revision)
            db.session.commit()
        except RevisionService.RevisionServiceException as exc:
            db.session.rollback()
            error(unicode(exc))
            abort(404, message=unicode(exc))
        except Exception as exc:
            error(unicode(exc))
            db.session.rollback()
            raise
        return "ok"


class RevisionItemResource(BaseCanoniseResource):
    model = RevisionItem
    attr_json = {
        'id': fields.Integer,
        'good_id': fields.Integer,
        'good': fields.String(attribute='good.full_name'),
        'revision_id': fields.Integer,
        # 'revision': fields.String(attribute="revision.name"),
        'count_before': fields.Integer,
        'count_after': fields.Integer,
    }


class RevisionResource(BaseCanoniseResource):
    model = Revision

    attr_json = {
        'id': fields.Integer,
        'date': Date,
        'pointsale_id': fields.Integer,
        'pointsale': fields.String(attribute="pointsale.name"),
        'seller_id': fields.Integer,
        'seller': fields.String(attribute="seller.name"),
    }

    def pre_save(self, obj, data):
        obj = super(RevisionResource, self).pre_save(obj, data)

        obj.date = HelperService.convert_to_pydate(data['date'])

        return obj

    def post_save(self, obj, data, create_new=False):
        super(RevisionResource, self).post_save(obj, data, create_new)

        if create_new:
            RevisionService.initial_revision(obj)

    def pre_delete(self, obj):

        pass
        # if RevisionService.exists_point(obj.pointsale_id, obj.id):
        #
        #     pass