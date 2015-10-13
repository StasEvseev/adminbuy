#coding: utf-8

__author__ = 'StasEvseev'


# from old.angular.field import DateFieldBootstrap, DecimalFieldBootstrap
# from old.angular.fieldview import FieldWidget
# from old.angular.urls import ResourceAngularUrl
# from old.angular.view import ModelProjectAngularView
# from applications.collection import CollectCanonResource
# from applications.collection.model import Collect
#
# from applications.point_sale.views import PointSaleAngularView
# from applications.seller.view import SellerAngularView
#
#
# class CollectAngularView(ModelProjectAngularView):
#     resource_view = ResourceAngularUrl("/api", "/collect", CollectCanonResource)
#     model = Collect
#
#     main_attrs = ('name', )
#
#     bread_attr = 'name'
#
#     dict_select_attr = 'name'
#
#     label_root = u"Инкассация"
#
#     form_columns = {
#         'date': DateFieldBootstrap(id="date", label=u"Дата сбора",
#                                    required=True),
#         'location': FieldWidget(col='location', label=u"Торговая точка",
#                                 view=PointSaleAngularView(), required=True, link="/admin/pointsaleangularview/"),
#         'seller': FieldWidget(col='seller', label=u"Продавец",
#                               view=SellerAngularView(), required=True, link="/admin/sellerangularview/"),
#         'sum': DecimalFieldBootstrap(id='sum', label=u"Сумма", required=True)
#     }
#     columns = (
#         (u'Дата сбора', 'date', "date: 'd MMM y'"),
#         (u'Торговая точка', 'location.name'),
#         (u'Продавец', 'seller.fullname'),
#         (u"Сумма", 'sum', 'rub')
#     )
#
#     grouping = (
#         (
#             (u'Параметры', ('date', 'location', 'seller', 'sum')),
#         ),
#     )
#
#     # tabs = (ocalViewWidget(view=GoodView(), attr="attrgoodlocal", title=u"Товары"),
#     # )
#     #     TableL