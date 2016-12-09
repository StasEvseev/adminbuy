# coding: utf-8

from adminbuy.applications.provider_app.models import Provider
from adminbuy.app import db

from ..suits import BaseSuite


__author__ = 'StasEvseev'


class ProviderTestSuite(BaseSuite):
    EMAIL = "stas@mail.ru"

    def create_test_provider(self):
        with self.application.app_context():
            provider = Provider(name='name', address='address',
                                emails=self.EMAIL)
            db.session.add(provider)
            db.session.commit()
            return (provider.id, provider.name, provider.address,
                    provider.emails)