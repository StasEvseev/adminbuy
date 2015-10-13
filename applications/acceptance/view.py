#coding: utf-8

__author__ = 'StasEvseev'

# from old.angular.field import CheckBox, BehaviorHiddenPredicate, DateFieldBootstrap
# from old.angular.field.validator import RequiredPredExpres
# from old.angular.fieldview import FieldWidget, TableLocalW
# from old.angular.urls import ResourceAngularUrl, ResourceAngularInnerUrl
# from old.angular.view import ModelProjectAngularView
#
# from applications.acceptance import AcceptanceCanon
# from applications.acceptance.extra import ExtraAcceptanceStatus, AcceptanceStatusExtra
# from applications.acceptance.fieldview import TableLocalImportsCondAcc, TableLocalWidgetAcc
# from applications.acceptance.model import Acceptance, AcceptanceItems
# from applications.acceptance.resource import AcceptanceItemInnerCanon
# from applications.invoice.view import InvoiceView, InvoiceItemsAcceptanceView
# from applications.point_sale.views import PointSaleAngularView
# from applications.provider_app.views import ProviderAngularView


# class AcceptanceItemView(ModelProjectAngularView):
#     """
#     Базовый View для позиций товара в инвентаризации.
#     """
#     resource_view = ResourceAngularInnerUrl('/api', '/acceptance', AcceptanceItemInnerCanon)
#     model = AcceptanceItems
#
#     dict_select_attr = 'good.full_name'
#
#     columns_edit_inline = (
#         (u"Наименование", 'good.full_name', (TableLocalW.OTHER, None, None)),
#         (u"Кол-во(накл.)", 'count', (TableLocalW.OTHER, None, None)),
#         (u"Кол-во(факт.)", 'fact_count', (TableLocalW.NUNMER_COL, None, None)),
#     )
#
#
# class AcceptanceNewView(ExtraAcceptanceStatus, ModelProjectAngularView):
#     resource_view = ResourceAngularUrl("/api", "/acceptance", AcceptanceCanon)
#     model = Acceptance
#
#     columns = (
#         (u'Дата', 'date', "date:'d MMM y'"),
#         (u"Накладная", 'invoice_str'),
#         (u"Поставщик", 'receiver'),
#         (u"Получатель", 'pointsale.name'),
#         (u"Статус", 'status_str')
#     )
#
#     form_columns = {
#         'type': CheckBox(id="type", label=u"Тип приемки", required=True, default_value=1, items=[
#             (1, u"Регулярные по почте"),
#             (2, u"Новая")
#         ]),
#         'date': DateFieldBootstrap(id="date", label=u"Дата приемки", required=True),
#         'pointsale': FieldWidget(
#             col='pointsale', label=u"Точка получатель", view=PointSaleAngularView(),
#             link="/admin/pointsaleangularview/"),
#         'invoice': FieldWidget(
#             col='invoice', label=u"Накладная", view=InvoiceView(), behaviors=[
#                 BehaviorHiddenPredicate('model.type == 2'),
#             ], validators=[RequiredPredExpres('type == 1', message=u"Заполните поле '%s'" % u"Накладная")],
#             can_create=False, can_edit=False),
#         'provider': FieldWidget(
#             col='provider', label=u"Поставшик", view=ProviderAngularView(), behaviors=[
#                 BehaviorHiddenPredicate('model.type == 1'),
#             ], validators=[RequiredPredExpres('type == 2', message=u"Заполните поле '%s'" % u"Постащик")],
#             link="/admin/providerangularview/"),
#     }
#
#     grouping = (
#         (
#             (u'Параметры приемки', ('date', 'pointsale', 'type', 'invoice', 'provider')),
#         ),
#     )
#
#     extra = (AcceptanceStatusExtra(), )
#
#     tabs = (
#         TableLocalImportsCondAcc(title=u"Продукты", view=AcceptanceItemView(), attr="items", remove=False),
#         TableLocalWidgetAcc(
#             title=u"Товар", view=InvoiceItemsAcceptanceView(), attr="new_items")
#     )