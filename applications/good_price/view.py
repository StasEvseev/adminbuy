#coding: utf-8

__author__ = 'StasEvseev'

# from old.angular.urls import ResourceGetAngularUrl
# from old.angular.view import ModelProjectAngularView
#
# from applications.price import PriceParishByGood2
# from applications.price.model import PriceParish
#
#
# class PriceToGoodView(ModelProjectAngularView):
#     model = PriceParish
#     resource_view = ResourceGetAngularUrl('/api', '/price/togood', PriceParishByGood2)
#
#     columns = (
#         (u"Номер накладной", 'invoice.number'),
#         (u"Поставщик", 'invoice.provider.name'),
#         (u"Дата", 'date_from', "date: 'd MMM y'"),
#         (u"Цена с НДС", 'price_post', 'rub'),
#         (u"Цена оптовая", 'price.price_gross', 'rub'),
#         (u"Цена розничная", 'price.price_retail', 'rub')
#     )
#
#     def get_urls(self):
#         return self.resource_view.url_get()