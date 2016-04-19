# coding: utf-8
from collections import defaultdict
import json
from sqlalchemy import desc
from applications.events.model import Event
from services.core import BaseSQLAlchemyModelService

__author__ = 'StasEvseev'


class EventService(BaseSQLAlchemyModelService):
    model = Event

    @classmethod
    def create_event(cls, user_id, datetime, type=model.MAIL, title_from='',
                     title='', body='', foot=''):
        data = {
            'title_from': title_from,
            'title': title,
            'body': body,
            'foot': foot
        }

        return cls.create_instance(
            type=type, datetime=datetime, user_id=user_id,
            date=json.dumps(data))

    @classmethod
    def get_events_by_user(cls, user_id):
        return cls.model.filter(cls.model.user_id == user_id)

    @classmethod
    def to_json(cls, events):
        events = events.order_by(desc(cls.model.datetime))
        result = defaultdict(list)
        for event in events:
            data = json.loads(event.data)
            date = event.datetime.date()
            time = event.datetime.time()
            item = {}
            item['time'] = time
            item['title_from'] = data.get('title_from', '')
            item['title'] = data.get('title', '')
            item['body'] = data.get('body', '')
            item['foot'] = data.get('foot', '')
            result[date].append(item)

        return result
