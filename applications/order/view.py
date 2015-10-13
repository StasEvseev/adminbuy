#coding: utf-8

__author__ = 'StasEvseev'

# from old.angular.field import DateFieldBootstrap
# from old.angular.fieldview import FieldWidget, TableLocalW
#
# from old.angular.urls import ResourceAngularInnerUrl, ResourceAngularUrl
# from old.angular.view import ModelProjectAngularView
#
# from applications.order import OrderCanon
# from applications.order.model import Order, OrderItem
# from applications.order.resource import OrderItemInnerCanon
# from applications.provider_app.views import ProviderAngularView
#
#
# class OrderItemView(ModelProjectAngularView):
#     resource_view = ResourceAngularInnerUrl("/api", "/order", OrderItemInnerCanon)
#     model = OrderItem
#
#     columns_edit_inline = (
#         (u"Наименование", 'full_name', (TableLocalW.OTHER, None, None)),
#         (u"Дата выхода", 'date', (TableLocalW.OTHER, "date:'d MMM y'", None)),
#         (u"Рем.", 'remission', (TableLocalW.OTHER, None, None)),
#         (u"Кол-во", 'count', (TableLocalW.NUNMER_COL, None, None)),
#         (u"Цена пред", 'price_prev', (TableLocalW.OTHER, 'rub', None)),
#         (u"Цена пост", 'price_post', (TableLocalW.OTHER, 'rub', None))
#     )
#
#
# class OrderView(ModelProjectAngularView):
#     resource_view = ResourceAngularUrl("/api", "/order", OrderCanon)
#     model = Order
#
#     dict_select_attr = 'id'
#
#     can_create = False
#
#     columns = (
#         (u"Поставшик", 'provider.name'),
#         (u"Дата от", 'date_start', "date:'d MMM y'"),
#         (u"Дата до", 'date_end', "date:'d MMM y'")
#     )
#
#     bread_attr = 'provider.name'
#
#     main_attrs = ('provider',)
#
#     form_columns = {
#         'provider': FieldWidget(col='provider', label=u"Поставщик", view=ProviderAngularView(),
#                                 required=True),
#         'date_start': DateFieldBootstrap(id="date_start", label=u"Дата от", required=True),
#         'date_end': DateFieldBootstrap(id='date_end', label=u"Дата до", required=True),
#     }
#
#     grouping = (
#         (
#             (u'Даты заказа', ('date_start', 'date_end')),
#         ),
#     )
#
#     tabs = (
#         TableLocalW(
#             title=u"Продукты", view=OrderItemView(), attr="items", remove=False),
#     )