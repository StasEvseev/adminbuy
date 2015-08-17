#coding: utf-8
from flask.ext import login

from admin._remove.baseview import BaseViewAuth
from angular.view import ProjectAngularView
from models.good import Good


class GoodView(BaseViewAuth):

    form_columns = ('full_name', 'barcode', )
    column_labels = {
        'full_name': u'Полное наименование',
        'barcode': u"Штрих код",
        'is_confirm': u'Товар получен',
        'invoiceitem.invoice.number': u'Накладная',
        'invoiceitem.invoice.provider.name': u'Поставщик',
        'invoiceitem.invoice.acceptance.date': u'Дата приема'}
    column_list = ('full_name', 'barcode', 'is_confirm', 'invoiceitem.invoice.acceptance.date',
                   'invoiceitem.invoice.number', 'invoiceitem.invoice.provider.name')
    can_delete = False
    can_create = False
    can_edit = False
    column_filters = ('full_name', 'barcode')

    # def is_accessible(self):
    #     return login.current_user.is_authenticated()

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(GoodView, self).__init__(Good, session, **kwargs)


class GoodViewPoint(ProjectAngularView):
    def index_view(self):
        return self.render('good/good.html',
                           token=login.current_user.generate_auth_token())