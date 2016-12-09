# coding: utf-8

from flask import request, g
from flask.ext.restful import fields, marshal_with

from adminbuy.db import db
from adminbuy.resources.core import BaseCanoniseResource, BaseTokeniseResource

from .model import Profile
from .service import SettingsService


__author__ = 'StasEvseev'


class BaseCanonWithoutId(BaseCanoniseResource):

    @classmethod
    def _register_into_rest(cls):
        self = cls()
        type1 = type(
            cls.__name__ + "Item",
            (BaseTokeniseResource, ),
            {
                "get": marshal_with(cls.attr_json)(self.get.__func__).__get__(
                    self, cls),
                "post": marshal_with(cls.attr_response_post)(
                    self.post.__func__).__get__(self, cls),
            }
        )

        return (
            (cls.prefix_url_without_id, type1),
        )


class ProfileCanon(BaseCanonWithoutId):
    model = Profile

    attr_json = {
        'id': fields.Integer,
        "rate_retail": fields.String,
        "rate_gross": fields.String,
    }

    prefix_url_with_id = ""

    def get(self):
        user = g.user

        return SettingsService.setting_to_user(user)

    def post(self):
        data = request.json['data']
        user = g.user

        profile = SettingsService.setting_to_user(user)
        profile.rate_gross = data['rate_gross']
        profile.rate_retail = data['rate_retail']

        db.session.add(profile)
        db.session.commit()

        return profile
