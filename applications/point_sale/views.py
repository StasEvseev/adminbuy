#coding: utf-8

__author__ = 'StasEvseev'

# from old.angular.field import TextFieldBootstrap
# from old.angular.fieldview import TableLocalViewWidget
# from old.angular.urls import ResourceAngularUrl, ResourceAngularInnerUrl
# from old.angular.view import ModelProjectAngularView
# from applications.point_sale.models import PointSale, PointSaleItem
# from applications.point_sale.resource import PointSaleCanon, PointSaleItemInnerCanon
# from applications.pointsale_good.view import GoodPointView
#
#
# class PointSaleItemView(ModelProjectAngularView):
#     resource_view = ResourceAngularInnerUrl("/api", "/pointsale", PointSaleItemInnerCanon)
#     model = PointSaleItem
#
#     dict_select_attr = 'good.full_name'
#
#     columns = (
#         (u"Наименование", 'good.full_name'),
#         (u"Количество", 'count')
#     )
#
#
# class PointSaleAngularView(ModelProjectAngularView):
#     resource_view = ResourceAngularUrl("/api", "/pointsale", PointSaleCanon)
#     model = PointSale
#
#     label_root = u"Точки"
#
#     form_columns = {'name': TextFieldBootstrap(id='name', label=u"Наименование", placeholder=u"Введите наименование",
#                                                required=True),
#                     'address': (u"Адрес", u"Введите адрес"),
#                     'is_central': (u"Центральная точка", u"")
#                     }
#
#     grouping = (
#         (
#             ("", ('address', 'is_central'),), #ModelProjectAngularView.EMPTY_COL
#         ),
#     )
#
#     main_attrs = ('name', )
#
#     dict_select_attr = 'name'
#
#     columns = (
#         (u'Наименование', 'name'),
#         (u'Адрес', 'address'),
#     )
#
#     tabs = (
#         TableLocalViewWidget(view=GoodPointView(), attr="attrgoodlocal", title=u"Товары", attr_id='inner_id',
#                              search=True, redir="'/admin/goodviewangular/' + obj.good_id + '/edit'"),
#     )