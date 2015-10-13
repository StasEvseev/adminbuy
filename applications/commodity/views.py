#coding: utf-8

__author__ = 'StasEvseev'

# from old.angular.field import TextFieldBootstrap, BooleanBootstrap
# from old.angular.fieldview import TableLocalViewWidget
# from old.angular.urls import ResourceAngularUrl
# from old.angular.view import ModelProjectAngularView
#
# from applications.commodity.models import Commodity
# from applications.commodity.resource import CommodityCanonResource
# from applications.good_commodity.view import GoodView
#
#
# class CommodityAngularView(ModelProjectAngularView):
#     resource_view = ResourceAngularUrl("/api", "/commodity", CommodityCanonResource)
#     model = Commodity
#
#     main_attrs = ('name', )
#
#     dict_select_attr = 'name'
#
#     label_root = u"Номенклатура"
#
#     form_columns = {'name': TextFieldBootstrap(id="name", label=u"Наименование", placeholder=u"Введите наименование",
#                                                required=True),
#                     'thematic': (u"Тематика", u"Введите тематику"),
#                     'numeric': BooleanBootstrap(id='numeric', label=u"Номерная", is_check=True)}
#     columns = (
#         (u'Наименование', 'name'),
#         (u'тематика', 'thematic'),
#         (u'Номерная', 'num')
#     )
#
#     tabs = (
#         TableLocalViewWidget(view=GoodView(), attr="attrgoodlocal", title=u"Товары"),
#     )