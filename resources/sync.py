#coding: utf-8
from dateutil import parser
import datetime
from flask import request
from flask.ext.restful import abort
from db import db

from models.sync import Sync, IN_PROGRESS, COMPLETE, SyncSession, SyncItemSession

from resources.core import BaseTokeniseResource


class SyncSessionRes(BaseTokeniseResource):
    def post(self):
        try:

            x = 1
            # deviceId = request.headers.environ.get("HTTP_DEVICEID")
            #
            # items = request.json['data']['items']
            #
            # sync = SyncSession()
            # sync.datetime = datetime.datetime.now()
            # sync.deviceId = deviceId
            # db.session.add(sync)
            #
            # for item in items:
            #
            #     s_item = SyncItemSession()
            #
            #     dt = parser.parse(item['datetime'])
            #     bc = item['barcode']
            #     op = item['operation']
            #     cnt = item['count']
            #
            #     s_item.sync = sync
            #     s_item.barcode = bc
            #     s_item.datetime = dt
            #     s_item.operation = op
            #     s_item.count = cnt
            #     db.session.add(s_item)
            #
            # db.session.commit()
            return "ok"
        except Exception as exc:
            abort(400, message="BLA")


class SyncResourceCreate(BaseTokeniseResource):
    def get(self):
        print "SYNC"
        sync = Sync()
        sync.date_start = datetime.datetime.now()
        sync.status = IN_PROGRESS
        db.session.add(sync)
        db.session.commit()

        return {"id": sync.id}


class SyncResource(BaseTokeniseResource):
    def post(self, invoice_id):
        print "POST SYNC"
        sync = Sync.query.get(invoice_id)
        sync.date_end = datetime.datetime.now()
        sync.status = COMPLETE
        db.session.add(sync)
        db.session.commit()
        return "ok"


class SyncResourceError(BaseTokeniseResource):
    def post(self, invoice_id, status):
        sync = Sync.query.get(id)
        sync.date_end = datetime.datetime.now()
        sync.status = status
        db.session.add(sync)
        db.session.commit()
        return "ok"