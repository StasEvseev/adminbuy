#coding:utf-8

import datetime
from collections import namedtuple

import xlrd

Product = namedtuple("Product", [
    'full_name', 'name', 'number_local', 'number_global', 'count_order', 'count_postorder', 'count',
    'price_without_NDS', 'price_with_NDS', 'sum_without_NDS', 'sum_NDS', 'rate_NDS', 'sum_with_NDS', 'thematic',
    'count_whole_pack', 'placer'], verbose=False)

ProductOrder = namedtuple("ProductOrder", [
    'full_name', 'name', 'number_local', 'number_global', 'date', 'remission', 'NDS', 'price_prev', 'price_post'
])

ProductReturn = namedtuple("ProductReturn", [
    'full_name', 'name', 'number_local', 'number_global', 'date', 'date_to', 'price_without_NDS',
    'price_with_NDS', 'remission', 'count_delivery', 'count_rem'
])


def get_value(sheet, col, row, mask_begin='_', mask_end='_'):
    cell = sheet.cell(col, row)
    value = cell.value
    if isinstance(value, float):
        return value
    result = substring(value, mask_begin, mask_end)
    return result


def substring(string, mask_begin, mask_end):
    ind_begin = string.find(mask_begin) + len(mask_begin)
    ind_end = string.find(mask_end)
    if not ind_end or ind_end == -1:
        result = string[ind_begin:]
    else:
        result = string[ind_begin:ind_end].strip()
    return result


def get_name_number(full_name):
    """
    Извлечь чистое имя, локальный и глобальный номера.
    """
    wt_nb = full_name.find(u"б/н")

    if wt_nb != -1:
        return full_name, None, None

    st = full_name.split(u"№")
    name = st[0].strip()
    number_local = st[1].split(u"(")[0]
    number_global = substring(st[1], "(", ")")
    return name, number_local, number_global


class InvoiceFabric(object):
    @classmethod
    def fabric(cls, file):
        doc = xlrd.open_workbook(file, on_demand=True, encoding_override="cp1251")
        sheet = doc.sheet_by_index(0)
        value = get_value(sheet, 3, 0)
        if value.startswith(u"Расходная накладная"):
            return InvoiceModel(file)
        elif get_value(sheet, 1, 0).startswith(u"Лист заказ"):
            # value =
            # if value:
            return InvoiceOrderModel(file)
        elif get_value(sheet, 1, 4).startswith(u"Список товаров, которые необходимо вернуть"):
            return InvoiceReturnModel(file)


class MailFile(object):
    def __init__(self, doc):
        self.doc = xlrd.open_workbook(doc, on_demand=True, encoding_override="cp1251")

    def handle(self, provider, mail):

        pass

    def find_cell(self, sheet, text):
        for rownum in range(sheet.nrows):
            row = sheet.row_values(rownum)
            if text in row:
                return rownum


class InvoiceModel(MailFile):
    """
    Класс для работы с файлом приходной накладной.
    """
    def __init__(self, doc):
        super(InvoiceModel, self).__init__(doc)

        self.count = 0
        self.start_row = 0

        sheet = self.doc.sheet_by_index(0)

        self.number = get_value(sheet, 3, 0, u'№ ', u' от')
        self.date = get_value(sheet, 3, 0, u'от', ' (')

        self.date = datetime.datetime.strptime(self.date, '%d.%m.%y').date()
        self.start_row = self.find_cell(sheet, u"Название издания") + 1
        row_ = self.find_cell(sheet, u'Итого:')
        self.count = row_ - self.start_row
        self.sum_without_NDS = get_value(sheet, row_, 7)
        self.sum_with_NDS = get_value(sheet, row_, 10)
        self.sum_NDS = get_value(sheet, row_, 9)

        row_ = row_ + 4
        self.weight = float(get_value(sheet, row_, 0, u'Вес товара - ', u'кг.'))

        row_ += 2
        self.responsible = get_value(sheet, row_, 0, u" /", u"/ ")

        assert self.number is not None
        assert self.date is not None
        assert self.sum_without_NDS is not None
        assert self.sum_with_NDS is not None
        assert self.sum_NDS is not None
        assert self.weight is not None
        assert self.responsible is not None

        # assert self.number and self.date and self.sum_without_NDS and self.sum_with_NDS and self.sum_NDS and self.weight and self.responsible

    def get_products(self):
        """
        Получим все позиции приходной накладной в виде списка объектов заглушек.
        """
        sheet = self.doc.sheet_by_index(0)
        result = []
        for rownum in range(self.start_row, self.start_row + self.count):
            if sheet.cell(rownum, 0).value != '':
                full_n = sheet.cell(rownum, 1).value
                arg = {}
                arg['full_name'] = full_n
                arg['name'], arg['number_local'], arg['number_global'] = get_name_number(full_n)
                arg['count_order'] = int(sheet.cell(rownum, 2).value)
                arg['count_postorder'] = int(sheet.cell(rownum, 3).value)
                arg['count'] = int(sheet.cell(rownum, 4).value)
                arg['price_without_NDS'] = sheet.cell(rownum, 5).value
                arg['price_with_NDS'] = sheet.cell(rownum, 6).value
                arg['sum_without_NDS'] = sheet.cell(rownum, 7).value
                arg['rate_NDS'] = sheet.cell(rownum, 8).value.replace(' %', '')
                arg['sum_NDS'] = sheet.cell(rownum, 9).value
                arg['sum_with_NDS'] = sheet.cell(rownum, 10).value
                arg['thematic'] = sheet.cell(rownum, 11).value

                if arg['rate_NDS'] == u'Без НДС':
                    arg['sum_NDS'] = 0
                    arg['rate_NDS'] = 0

                count_whole_pack = sheet.cell(rownum, 12).value
                if count_whole_pack in ['   ', '  ', ' ', ''] :
                    count_whole_pack = 0
                else:
                    count_whole_pack = int(count_whole_pack)
                arg['count_whole_pack'] = count_whole_pack
                placer = sheet.cell(rownum, 13).value
                if isinstance(placer, (str, unicode)):
                    arg['placer'] = 0
                else:
                    arg['placer'] = int(placer)

                ip = Product(**arg)
                result.append(ip)
            else:
                return result
        return result

    def handle(self, provider, mail):
        from adminbuy.services.mailinvoice import InvoiceService
        from adminbuy.db import db
        invmodel = InvoiceService.create_invoice(
            number=self.number, date=self.date, provider=provider,
            sum_without_NDS=self.sum_without_NDS, sum_with_NDS=self.sum_with_NDS,
            sum_NDS=self.sum_NDS, weight=self.weight, responsible=self.responsible)
        products = self.get_products()

        mail.invoice = invmodel

        db.session.add(mail)

        for product in products:
            InvoiceService.handle_invoiceitem(
                full_name=product.full_name, name=product.name, number_local=product.number_local,
                number_global=product.number_global,
                count_order=product.count_order, count_postorder=product.count_postorder,
                count=product.count, price_without_NDS=product.price_without_NDS,
                price_with_NDS=product.price_with_NDS, sum_without_NDS=product.sum_without_NDS,
                sum_NDS=product.sum_NDS, rate_NDS=product.rate_NDS, sum_with_NDS=product.sum_with_NDS,
                thematic=product.thematic, count_whole_pack=product.count_whole_pack,
                placer=product.placer, invoice=invmodel)


class InvoiceOrderModel(MailFile):

    def __init__(self, doc):
        super(InvoiceOrderModel, self).__init__(doc)

        self.count = 0
        self.start_row = 0

        sheet = self.doc.sheet_by_index(0)

        self.date_from = get_value(sheet, 2, 0, u'емые  c ', u' по')
        self.date_to = get_value(sheet, 2, 0, u'по ')

        self.date_from = datetime.datetime.strptime(self.date_from, '%d.%m.%y').date()
        self.date_to = datetime.datetime.strptime(self.date_to, '%d.%m.%y').date()
        self.start_row = self.find_cell(sheet, u"Название издания") + 2
        row_ = self.find_cell(sheet, u'* все цены указаны с учетом НДС')
        self.count = row_ - self.start_row
        assert self.count and self.date_from and self.date_to and self.start_row

    def get_products(self):
        """
        Получим все позиции приходной накладной в виде списка объектов заглушек.
        """
        sheet = self.doc.sheet_by_index(0)
        result = []
        for rownum in range(self.start_row, self.start_row + self.count):
            if sheet.cell(rownum, 0).value != '':
                full_n = sheet.cell(rownum, 1).value
                arg = {}
                arg['full_name'] = full_n
                arg['name'], arg['number_local'], arg['number_global'] = get_name_number(full_n)
                arg['date'] = datetime.datetime.strptime(sheet.cell(rownum, 3).value, '%d.%m.%y').date()
                arg['remission'] = int(sheet.cell(rownum, 4).value) if sheet.cell(rownum, 4).value.strip() not in ['', ' '] else 0
                arg['NDS'] = sheet.cell(rownum, 5).value
                arg['price_prev'] = sheet.cell(rownum, 7).value
                arg['price_post'] = sheet.cell(rownum, 8).value

                ip = ProductOrder(**arg)
                result.append(ip)
            else:
                return result
        return result

    def handle(self, provider, mail):
        from applications.order.service import OrderService
        from adminbuy.db import db
        order = OrderService.create_order(date_start=self.date_from, date_end=self.date_to, provider_id=provider.id)

        products = self.get_products()
        mail.order = order
        db.session.add(mail)

        for product in products:
            OrderService.handle_orderitem(
                full_name=product.full_name, name=product.name, number_local=product.number_local,
                number_global=product.number_global, date=product.date, remission=product.remission, NDS=product.NDS,
                price_prev=product.price_prev, price_post=product.price_post, order=order)


class InvoiceReturnModel(MailFile):

    def _date(self, sheet):
        count_attempt = 5
        from_, to_ = None, None
        row = 2

        while count_attempt:
            date_from = get_value(sheet, row, 4, u'c : ', u' по ')
            date_to = get_value(sheet, row, 4, u' по ')
            try:
                from_ = datetime.datetime.strptime(date_from, '%d.%m.%y').date()
                to_ = datetime.datetime.strptime(date_to, '%d.%m.%y').date()
            except UnicodeEncodeError:
                count_attempt -= 1
                row += 1
            else:
                break
        if from_ is None or to_ is None:
            raise Exception(u"Не удалось получить даты.")
        return from_, to_

    def __init__(self, doc):
        super(InvoiceReturnModel, self).__init__(doc)

        self.count = 0
        self.start_row = 0

        sheet = self.doc.sheet_by_index(0)

        self.date_from, self.date_to = self._date(sheet)#get_value(sheet, 2, 4, u'c : ', u' по ')
        #self.date_to = get_value(sheet, 2, 4, u' по ')

        #self.date_from = datetime.datetime.strptime(self.date_from, '%d.%m.%y').date()
        #self.date_to = datetime.datetime.strptime(self.date_to, '%d.%m.%y').date()
        self.start_row = self.find_cell(sheet, u"Название издания") + 1
        # row_ = self.find_cell(sheet, u'* все цены указаны с учетом НДС')
        # self.count = row_ - self.start_row
        assert self.date_from and self.date_to and self.start_row

    def get_products(self):
        """
        Получим все позиции приходной накладной в виде списка объектов заглушек.
        """
        sheet = self.doc.sheet_by_index(0)
        result = []
        for rownum in range(self.start_row, self.start_row + 10000):
            try:
                ind_v = sheet.cell(rownum, 1).value
            except IndexError:
                return result
            if ind_v != '':
                full_n = sheet.cell(rownum, 2).value
                arg = {}
                arg['full_name'] = full_n
                arg['name'], arg['number_local'], arg['number_global'] = get_name_number(full_n)
                arg['date'] = datetime.datetime.strptime(sheet.cell(rownum, 3).value, '%d.%m.%y').date()
                arg['date_to'] = datetime.datetime.strptime(sheet.cell(rownum, 4).value, '%d.%m.%y').date()
                arg['price_without_NDS'] = float(sheet.cell(rownum, 5).value)
                arg['price_with_NDS'] = float(sheet.cell(rownum, 6).value)
                arg['remission'] = int(sheet.cell(rownum, 7).value) if sheet.cell(rownum, 4).value.strip() not in ['', ' '] else 0
                arg['count_delivery'] = int(sheet.cell(rownum, 8).value)
                arg['count_rem'] = int(sheet.cell(rownum, 9).value)

                ip = ProductReturn(**arg)
                result.append(ip)
            else:
                return result
        return result

    def handle(self, provider, mail):
        from applications.return_app.service import ReturnService
        from adminbuy.db import db
        return_inst = ReturnService.create_return(date_start=self.date_from, date_end=self.date_to, provider_id=provider.id)

        products = self.get_products()
        mail.return_item = return_inst
        db.session.add(mail)

        for product in products:
            ReturnService.handle_returnitem(
                full_name=product.full_name, name=product.name, number_local=product.number_local,
                number_global=product.number_global, date=product.date, date_to=product.date_to,
                price_without_NDS=product.price_without_NDS, price_with_NDS=product.price_with_NDS,
                remission=product.remission, count_delivery=product.count_delivery, count_rem=product.count_rem,
                return_inst=return_inst)