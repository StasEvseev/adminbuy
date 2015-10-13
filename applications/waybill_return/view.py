#coding: utf-8

__author__ = 'StasEvseev'

# from old.angular.field import CheckBox, TextFieldBootstrap, DateFieldBootstrap, BehaviorHiddenPredicate
# from old.angular.field.validator import RequiredPredExpres
# from old.angular.fieldview import FieldWidget, TableLocalW
# from old.angular.urls import ResourceAngularUrl, ResourceAngularInnerUrl, ResourceGetAngularUrl
# from old.angular.view import ModelProjectAngularView
#
# from applications.point_sale.views import PointSaleAngularView
# from applications.receiver.view import ReceiverAngularView
# from applications.return_app.view import ReturnView
# from applications.waybill_return import WayBillReturnItemInnerCanon, WayBillReturnCanon
# from applications.waybill_return.extra import WaybillReturnStatusExtra, ExtraWayBillReturnStatus
# from applications.waybill_return.fieldview import TableLocalImportsCondWayRet
# from applications.waybill_return.model import WayBillReturnItems, WayBillReturn
# from applications.waybill_return.resource import WayBillReturnPrint
#
#
# class WayBillReturnItemView(ModelProjectAngularView):
#     resource_view = ResourceAngularInnerUrl("/api", "/waybillreturn", WayBillReturnItemInnerCanon)
#     model = WayBillReturnItems
#
#     dict_select_attr = 'good.full_name'
#
#     columns_edit_inline = (
#         (u"Наименование", 'good.full_name', (TableLocalW.OTHER, None, None)),
#         (u"Кол-во прислано", 'count_plan', (TableLocalW.OTHER, None, None)),
#         (u"Кол-во", 'count', (TableLocalW.NUNMER_COL, None, None)),
#     )
#
#
# class WayBillReturnView(ExtraWayBillReturnStatus, ModelProjectAngularView):
#     resource_view = ResourceAngularUrl("/api", "/waybillreturn", WayBillReturnCanon)
#     resource_print = ResourceGetAngularUrl("/api", "/waybillreturn/print", WayBillReturnPrint)
#     model = WayBillReturn
#
#     dict_select_attr = 'number'
#
#     main_attrs = ('number', )
#
#     form_columns = {
#         'type': CheckBox(id="type", label=u"Тип накладной", required=True, items=[
#             (1, u"Розничная"),
#             (2, u"Оптовая")
#         ]),
#         'typeRec': CheckBox(id="typeRec", label=u"Получатель", required=True, default_value=1, items=[
#             (1, u"Товарные точки"),
#             (2, u"Оптовики"),
#         ]),
#         'receiver': FieldWidget(
#             col="receiver", label=u"Оптовики", view=ReceiverAngularView(), behaviors=[
#                 BehaviorHiddenPredicate('model.typeRec == 1'),
#             ], validators=[RequiredPredExpres('typeRec == 2', message=u"Заполните поле '%s'" % u"Оптовики")]
#         ),
#         'pointsale': FieldWidget(
#             col='pointsale', label=u"Торговая точка получатель", view=PointSaleAngularView(), behaviors=[
#                 BehaviorHiddenPredicate('model.typeRec == 2'),
#             ], validators=[RequiredPredExpres('typeRec == 1',
#                                               message=u"Заполните поле '%s'" % u"Торговая точка получатель")]
#         ),
#         'returninst': FieldWidget(
#             col="returninst", label=u"Накладная возврата", view=ReturnView(), required=True, can_create=False, can_edit=False
#         ),
#         'date': DateFieldBootstrap(id="date", label=u"Дата накладной", required=True),
#         'date_to': DateFieldBootstrap(id="date_to", label=u"Дата возврата", required=True),
#         'number': TextFieldBootstrap(
#             id='number', label=u"Номер накладной", behaviors=[
#                 BehaviorHiddenPredicate('model.id == undefined'),
#             ])
#     }
#
#     grouping = (
#         (
#             (u"Параметры накладной", ('date', 'date_to', 'type')),
#             (u"Получатели", ('typeRec', 'pointsale', 'receiver'))
#         ),
#         (
#             (u"Основание", ('returninst', )),
#
#         )
#     )
#
#     extra = (WaybillReturnStatusExtra(), )
#
#     tabs = (
#         TableLocalImportsCondWayRet(title=u"Продукты", view=WayBillReturnItemView(), attr="items",
#                                  remove=True),
#     )
#
#     columns = (
#         (u'Дата', 'date', "date:'d MMM y'"),
#         (u'Номер', 'number'),
#         (u"Получатель", "rec"),
#         (u"Основание", "returninst.name"),
#         (u"Тип", "type_str"),
#         (u"Статус", 'status_str')
#     )
