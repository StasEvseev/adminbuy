# coding: utf-8

from flask.ext import restful
from flask.ext.restful.fields import Raw
from log import error


class Date(Raw):
    def format(self, value):
        return value.isoformat()


class MyApi(restful.Api):
    def register_canon(self, canon_res, url):
        try:
            res_urls = canon_res._register_into_rest()
            for rurl in res_urls:
                url_1, res1 = rurl
                canon_res.fill_url = self.prefix + url
                self.add_resource(res1, url + url_1)
        except Exception as exc:
            error(u"Ошибка при регистрации REST points. " + unicode(exc))
            raise exc

    def register_getall(self, getallres, url):
        try:
            res = getallres._register_into_rest()
            self.add_resource(res, url)
        except Exception as exc:
            error(u"Ошибка при регистрации REST points. " + unicode(exc))
            raise exc

api = MyApi(prefix='/api')


from resources.core import (TokenResource, AuthResource, RegistrationResource,
                            ProfileResource, IdentityResource)
from resources.invoice import (InvoicePriceItemsResource, InvoiceItemResource,
                               InvoiceItemCountResource,
                               InvoicePrice2ItemsResource)
from resources.sync import (SyncResource, SyncResourceError,
                            SyncResourceCreate, SyncSessionRes)
from resources.revision import (RevisionResource, RevisionItemResource,
                                RevisionApprove)

from resources.core import TokenResource, AuthResource, RegistrationResource, \
    ProfileResource, IdentityResource, ProfileResourceById
from resources.invoice import (
    InvoicePriceItemsResource, InvoiceItemResource, InvoiceItemCountResource,
    InvoicePrice2ItemsResource)
from resources.sync import (SyncResource, SyncResourceError, SyncResourceCreate,
                            SyncSessionRes)
from resources.revision import (RevisionResource, RevisionItemResource,
                                RevisionApprove)
from applications.mails.resource import MailCheck, MailInvoiceItem, MailItem

api.add_resource(RegistrationResource, '/registration')
api.add_resource(TokenResource, '/token')
api.add_resource(AuthResource, '/auth')
api.add_resource(IdentityResource, '/identity')
api.add_resource(ProfileResource, '/profile')
api.add_resource(ProfileResourceById, '/profile_by_id/<int:id>')

api.add_resource(MailCheck, '/mail')
api.add_resource(MailItem, '/mail/<int:id>')
api.add_resource(MailInvoiceItem, '/mail/<int:id>/items')

api.add_resource(InvoiceItemResource, '/invoice/<int:invoice_id>/items')
api.add_resource(InvoiceItemCountResource, '/invoice/<int:invoice_id>/count')

api.add_resource(InvoicePrice2ItemsResource, '/invoiceprice2items/<int:id>')

api.add_resource(SyncSessionRes, '/syncSession')

api.add_resource(SyncResourceCreate, '/sync/new')
api.add_resource(SyncResource, '/sync/<int:invoice_id>/stop')
api.add_resource(
    SyncResourceError, '/sync/<int:invoice_id>/status/<int:status>')

api.register_canon(RevisionResource, '/revision')
api.register_canon(RevisionItemResource, '/revisionitem')
api.add_resource(RevisionApprove, '/revision/<int:id>/approve')
