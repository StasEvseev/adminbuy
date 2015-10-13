#coding: utf-8

__author__ = 'StasEvseev'

# from old.angular.field import TextFieldBootstrap
# from old.angular.urls import ResourceAngularUrl
# from old.angular.view import ModelProjectAngularView
#
# from applications.provider_app.models import Provider
# from applications.provider_app.resource import ProviderCanon
#
#
# class ProviderAngularView(ModelProjectAngularView):
#     # from resources.provider import ProviderCanon
#     resource_view = ResourceAngularUrl("/api", "/provider", ProviderCanon)
#     model = Provider
#     main_attrs = ('name', )
#     dict_select_attr = 'name'
#
#     label_root = u"Поставщики"
#
#     form_columns = {'name': TextFieldBootstrap(id="name", label=u"Наименование", placeholder=u"Введите наименование",
#                                                required=True),
#                     'address': (u"Адрес", u"Введите адрес"),
#                     'emails': (u"Почтовые ящики", u"Введите адреса(через запятую)")}
#     columns = (
#         (u'Наименование', 'name'),
#         (u'Адрес', 'address'),
#         (u'Почтовые ящики', 'emails')
#     )