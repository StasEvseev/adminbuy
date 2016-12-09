# coding: utf-8

import datetime

from dateutil import parser
from flask import request
from flask.ext.restful import abort

from adminbuy.db import db

from adminbuy.models.sync import (Sync, SyncSession, SyncItemSession,
                                  IN_PROGRESS, COMPLETE)

from adminbuy.resources.core import BaseTokeniseResource

from adminbuy.services.syncservice import SyncService
from adminbuy.services.userservice import UserService

__author__ = 'StasEvseev'


class SyncSessionRes(BaseTokeniseResource):
    def post(self):
        """
        Синхронизация Рабочего Места с сервером.

        Для синхронизации требуется помещать в заголовки DeviceId.


        """
        try:
            deviceId = request.headers.environ.get("HTTP_DEVICEID")

            workday_items = request.json['data']['items']

            sync = SyncSession()
            sync.datetime = datetime.datetime.now()
            sync.deviceId = deviceId
            db.session.add(sync)

            for workday_item in workday_items:
                user = UserService.get_by_name(workday_item['username'])
                datetime_start = parser.parse(workday_item['date_start'])

                workday = SyncService.get_or_create(user.id, datetime_start)

                if not workday.id:
                    workday.sync_start = sync

                if workday_item['date_end']:
                    workday.datetime_end = parser.parse(
                        workday_item['date_end'])
                    workday.sync_end = sync
                workday.username = workday_item['username']
                db.session.add(workday)

                for item in workday_item['items']:
                    dt = parser.parse(item['datetime'])
                    bc = item['barcode']
                    op = item['operation']
                    cnt = item['count']

                    s_item = SyncItemSession()
                    s_item.sync = sync
                    s_item.workday = workday
                    s_item.barcode = bc
                    s_item.datetime = dt
                    s_item.operation = op
                    s_item.count = cnt
                    db.session.add(s_item)
            db.session.commit()
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
