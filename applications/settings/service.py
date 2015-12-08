# coding: utf-8

from applications.settings.model import Profile
from db import db
from services.core import BaseSQLAlchemyModelService

__author__ = 'StasEvseev'


class SettingsService(BaseSQLAlchemyModelService):
    model = Profile

    @classmethod
    def setting_to_user(cls, user):
        profile = Profile.query.filter(
            Profile.user_id == user.id
        )
        if profile.count() == 0:
            profile = Profile()
            profile.user = user
            db.session.add(profile)
            db.session.commit()
        else:
            profile = profile.one()
        return profile
