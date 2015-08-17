#coding: utf-8
from app import db

from tests.helpers.suits import BaseSuite
from applications.provider_app.models import Provider

# import provider


class ProviderTestSuite(BaseSuite):
    EMAIL = "stas@mail.ru"

    def create_test_provider(self):
        with self.application.app_context():
            provider = Provider(name='name', address='address', emails=self.EMAIL)
            db.session.add(provider)
            db.session.commit()
            return provider.id, provider.name, provider.address, provider.emails