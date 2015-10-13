#coding: utf-8

__author__ = 'StasEvseev'

# from old.angular.urls import ResourceAngularInnerUrl
# from old.angular.view import ModelProjectAngularView
#
# from applications.good.model import Good
# from applications.point_sale import PointSaleItemInnerCanon
#
#
# class GoodPointView(ModelProjectAngularView):
#     model = Good
#     resource_view = ResourceAngularInnerUrl('/api', '/pointsale', PointSaleItemInnerCanon)
#
#     columns = (
#         (u"Полное наименование", 'full_name'),
#         (u"Кол-во", 'count'),
#         (u"Цена розничная", 'good.price.price_retail', 'rub')
#     )
#
#     def get_urls(self):
#         return self.resource_view.url_getall()