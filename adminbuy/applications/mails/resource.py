# coding: utf-8

from flask import request
from flask.ext.restful import abort, marshal_with, fields

from adminbuy.db import db
from adminbuy.excel import InvoiceModel, InvoiceReturnModel
from adminbuy.resources import core

from .model import Mail

from log import error, debug


__author__ = 'StasEvseev'


ITEM = {
        'id': fields.Integer,
        'date': fields.DateTime(dt_format='iso8601'),
        'title': fields.String,
        'from': fields.String(attribute='from_'),
        'is_handling': fields.Boolean,
        'text': fields.String,
        'order_id': fields.Integer,
        'return_id': fields.Integer,
        'invoice_id': fields.Integer,
        'provider_id': fields.Integer(attribute='invoice.provider_id'),
        'provider_name': fields.String,
        'files_': fields.List(fields.Nested({
            'name': fields.String,
            'link': fields.String
        }))
    }


class MailInvoiceItem(core.BaseTokeniseResource):
    def get(self, id):
        from adminbuy.applications.invoice import InvoiceItemResource
        from adminbuy.services.mailinvoice import MailInvoiceService
        mail = MailInvoiceService.get_mail(id)
        return InvoiceItemResource().get(mail.invoice_id)


class MailItem(core.BaseTokeniseResource):
    @marshal_with(ITEM)
    def get(self, id):
        from adminbuy.services.mailinvoice import MailInvoiceService
        mail = MailInvoiceService.get_mail(id)
        MailInvoiceService.handle(mail)
        db.session.add(mail)
        db.session.commit()
        return mail

    @marshal_with(ITEM)
    def post(self, id):
        from adminbuy.services.mailinvoice import MailInvoiceService
        action = request.json['action']
        index = request.json['index']

        debug(u"Обработка файла почты под индексом '%s' по типу '%s'" % (
            index, action))
        mail = MailInvoiceService.get_mail(id)
        file = mail.get_file_to_index(index)
        fpth = file['path']
        debug(u"Путь к файлу - '%s'" % fpth)
        if action == "R":
            if mail.invoice_id:
                debug(u"Файл уже был обработан.")
                return mail
            try:
                debug(u"Обработка файла.")
                m = InvoiceModel(fpth)
                m.handle(mail.provider, mail)
                mail.is_handling = True
                db.session.add(mail)
                db.session.commit()
                debug(u"Обработка файла завершена.")
            except Exception as err:
                error(
                    u"Ошибка при обработке файла '"+fpth+u"'. " + unicode(err))
                abort(400, message=u"Произошла ошибка в обработке документа.")
            else:
                return mail
        elif action == "V":
            if mail.return_id:
                debug(u"Файл уже был обработан.")
                return mail
            try:
                debug(u"Обработка файла.")
                m = InvoiceReturnModel(fpth)
                m.handle(mail.provider, mail)
                mail.is_handling = True
                db.session.add(mail)
                db.session.commit()
                debug(u"Обработка файла завершена.")
            except Exception as err:
                error(
                    u"Ошибка при обработке файла '"+fpth+u"'. " + unicode(err))
                abort(400, message=u"Произошла ошибка в обработке документа.")
            else:
                return mail


class MailCheck(core.BaseTokenMixinResource, core.BaseModelPackResource):
    """
    Ресурс для работы с почтой.
    """

    model = Mail

    default_sort = 'desc', 'id'

    multif = {}

    def post(self):
        """
        Запрос на обработку почтового ящика(проверка новых писем и сохранение
        их в БД).
        """
        from adminbuy.services.mailinvoice import MailInvoiceService, \
            MailInvoiceException
        try:
            res = MailInvoiceService.handle_mail()
        except MailInvoiceException as err:
            error(unicode(err))
            abort(400, message=unicode(err))
        res = 'ok' if len(res) else 'nothing'
        return res

    def filter_query(self, query, filter_field, filter_text, sort_field,
                     sort_course, page, count):
        """
        Метод для дополнительной фильтрации.
        """

        return core.FilterObj.filter_query(
            query, filter_field, filter_text, sort_field, sort_course, page,
            count, model=self.model, multif=self.multif, clazz=self.__class__,
            default_sort=self.default_sort)

    def query_initial(self, *args, **kwargs):
        _new = request.values.get("_new", "false") in ['true']
        if _new:
            return self.model.query.filter(self.model.is_handling == False)
        return self.model.query

    @marshal_with({'items': fields.List(fields.Nested(ITEM)),
                   'count': fields.Integer,
                   'max': fields.Integer})
    def get(self, *args, **kwargs):
        """
        Получим все почтовые письма.
        """
        args_pars = core.parser.parse_args()

        filter_field = args_pars['filter_field']
        filter_text = args_pars['filter_text']
        sort_field = args_pars['sort_field']
        sort_course = args_pars['sort_course']
        page = args_pars['page']
        count = args_pars['count']

        query = self.query_initial(*args, **kwargs)

        records, max_, count_ = self.filter_query(
            query, filter_field, filter_text, sort_field, sort_course, page,
            count)

        return {'items': records, 'count': count_, 'max': max_}
