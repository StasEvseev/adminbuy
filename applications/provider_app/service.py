# coding: utf-8

from applications.provider_app.models import Provider
from services.core import BaseSQLAlchemyModelService

__author__ = 'StasEvseev'


class ProviderService(BaseSQLAlchemyModelService):

    model = Provider

    # @classmethod
    # def get_by_id(cls, id):
    #     return Provider.query.get(id)

    @classmethod
    def get_all(cls):
        return Provider.query.all()

    @classmethod
    def get_provider_by_email(cls, email):
        return Provider.query.filter(
            Provider.emails.like('%'+ email +'%')).one()

    @classmethod
    def get_all_emails(cls):
        emails = []
        for provider in cls.get_all():
            emails.extend(provider.get_emails())
        return emails
