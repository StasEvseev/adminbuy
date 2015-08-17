#coding: utf-8
from sqlalchemy import or_

from admin._remove.baseview import BaseViewAuth
from models.acceptance import Acceptance

# from models.invoice import Invoice
from models.invoice import Invoice


class AcceptanceView(BaseViewAuth):
    form_columns = ('invoice', 'date')
    column_labels = dict(invoice=u'Накладная', date=u'Дата')
    can_delete = False

    # def is_accessible(self):
    #     return login.current_user.is_authenticated()

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(AcceptanceView, self).__init__(Acceptance, session, **kwargs)

    # def create_view(self):
    #
    #     pass


    def create_form(self, obj=None):

        form = super(AcceptanceView, self).create_form(obj)

        form.invoice.query_factory = Invoice.query.outerjoin(
            Invoice.acceptance
        ).filter(
            Acceptance.invoice_id == None
        ).all

        return form

    def edit_form(self, obj=None):

        form = super(AcceptanceView, self).edit_form(obj)

        form.invoice.query_factory = Invoice.query.outerjoin(
            Invoice.acceptance
        ).filter(
            or_(
                Acceptance.invoice_id == None,
                Invoice.id == obj.invoice_id
            )

        ).all

        return form