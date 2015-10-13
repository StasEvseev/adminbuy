# coding: utf-8
import json
from applications.events.service import EventService
from tests import BaseTestCase
from tests.helpers import Generator

__author__ = 'user'


class Mock(object):
    def __init__(self, lst):
        self.list = lst
    def __iter__(self):
        return iter(self.list)
    def order_by(self, p):
        return self


class TestEvents(BaseTestCase):

    def set_up(self):
        pass

    def test_to_json(self):

        data = json.dumps({
            'title': u"",
            "body": u"",
            "foot": u""
        })

        date_1 = Generator.generate_datetime()
        date_2 = Generator.generate_datetime()

        mock = Mock([
            EventService.create_instance(
                type=EventService.model.MAIL,
                datetime=date_1,
                user_id=1,
                data=data
            ),
            EventService.create_instance(
                type=EventService.model.MAIL,
                datetime=date_2,
                user_id=1,
                data=data
            ),
            EventService.create_instance(
                type=EventService.model.MAIL,
                datetime=date_1,
                user_id=1,
                data=data
            ),
        ])

        res = EventService.to_json(mock)

        self.assertEqual(len(res.keys()), 2)