#coding: utf-8

__author__ = 'StasEvseev'

# from old.angular.urls import ResourceGetAngularUrl
# from old.angular.view import ModelProjectAngularView
#
# from applications.good.model import Good
# from applications.good_commodity import GoodCommodityResource
#
#
# class GoodView(ModelProjectAngularView):
#     model = Good
#     resource_view = ResourceGetAngularUrl('/api', '/good/tocommodity', GoodCommodityResource)
#
#     columns = (
#         (u"Полное наименование", 'full_name'),
#         (u"Номер в пределах года", 'number_local'),
#         (u"Номер в пределах издания", 'number_global'),
#         (u"Цена оптовая", 'price.price_gross'),
#         (u"Цена розничная", 'price.price_retail')
#     )
#
#     def get_urls(self):
#         return self.resource_view.url_get()