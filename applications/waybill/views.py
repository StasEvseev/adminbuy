#coding: utf-8

from angular.field import CheckBox, TextFieldBootstrap, DateFieldBootstrap, BehaviorHiddenPredicate
from angular.field.validator import RequiredPredExpres
from angular.fieldview import FieldWidget, TableLocalW
from angular.urls import ResourceAngularUrl, ResourceAngularInnerUrl, ResourceGetAngularUrl
from angular.view import ModelProjectAngularView

from applications.point_sale.views import PointSaleAngularView
from applications.receiver.view import ReceiverAngularView
from applications.waybill import WayBillCanon, WayBillItemInnerCanon
from applications.waybill.extra import ExtraWayBillStatus, WaybillStatusExtra
from applications.waybill.fieldview import TableLocalImportsCondWay
from applications.waybill.models import WayBill, WayBillItems
from applications.waybill.importer import ImporterFromPointSale, ImporterFromInvoice
from applications.waybill.resource import WayBillPrint


class WayBillItemView(ModelProjectAngularView):
    resource_view = ResourceAngularInnerUrl("/api", "/waybill", WayBillItemInnerCanon)
    model = WayBillItems

    dict_select_attr = 'good.full_name'

    columns_edit_inline = (
        (u"Наименование", 'good.full_name', (TableLocalW.OTHER, None, None)),
        (u"Цена оптовая", 'good.price.price_gross', (TableLocalW.OTHER, "rub", "ng-hide='model.type == 1'")),
        (u"Цена розничная", 'good.price.price_retail', (TableLocalW.OTHER, "rub", "ng-hide='model.type == 2'")),
        (u"Кол-во", 'count', (TableLocalW.NUNMER_COL, None, None)),
        (u"Сумма", 'sum', (
            TableLocalW.CALC_COL,
            ("rub", "model.type == 1 ? item.count * item.good.price.price_retail : item.count * item.good.price.price_gross"),
            None))
    )


class WayBillView(ExtraWayBillStatus, ModelProjectAngularView):
    resource_view = ResourceAngularUrl("/api", "/waybill", WayBillCanon)
    resource_print = ResourceGetAngularUrl("/api", "/waybill/print", WayBillPrint)
    model = WayBill

    dict_select_attr = 'number'

    main_attrs = ('number', )

    form_columns = {
        'type': CheckBox(id="type", label=u"Тип накладной", required=True, items=[
            (1, u"Розничная"),
            (2, u"Оптовая")
        ]),
        'typeRec': CheckBox(id="typeRec", label=u"Получатель", required=True, default_value=1, items=[
            (1, u"Товарные точки"),
            (2, u"Оптовики"),
        ]),
        'pointsale_from': FieldWidget(
            col='pointsale_from', label=u"Торговая точка", view=PointSaleAngularView(), required=True,
            link="/admin/pointsaleangularview/"),
        'receiver': FieldWidget(
            col="receiver", label=u"Оптовики", view=ReceiverAngularView(), behaviors=[
                BehaviorHiddenPredicate('model.typeRec == 1'),
            ], validators=[RequiredPredExpres('typeRec == 2', message=u"Заполните поле '%s'" % u"Оптовики")],
            link="/admin/receiverangularview/"
        ),
        'pointsale': FieldWidget(
            col='pointsale', label=u"Торговая точка получатель", view=PointSaleAngularView(), behaviors=[
                BehaviorHiddenPredicate('model.typeRec == 2'),
            ], validators=[RequiredPredExpres('typeRec == 1',
                                              message=u"Заполните поле '%s'" % u"Торговая точка получатель")],
            link="/admin/pointsaleangularview/"
        ),
        'date': DateFieldBootstrap(id="date", label=u"Дата накладной", required=True),
        'number': TextFieldBootstrap(
            id='number', label=u"Номер накладной", behaviors=[
                BehaviorHiddenPredicate('model.id == undefined'),
            ])
    }

    grouping = (
        (
            (u"Параметры накладной", ('date', 'pointsale_from', 'type')),
            (u"Получатели", ('typeRec', 'pointsale', 'receiver'))
        ),
    )

    extra = (WaybillStatusExtra(), )

    tabs = (
        TableLocalImportsCondWay(title=u"Продукты", view=WayBillItemView(), attr="items", imports=[
            ImporterFromPointSale(), ImporterFromInvoice()
        ], remove=True),
    )

    columns = (
        (u'Дата', 'date', "date:'d MMM y'"),
        (u'Номер', 'number'),
        (u"Получатель", "rec"),
        (u"Отправитель", "pointsale_from"),
        (u"Тип", "type_str"),
        (u"Статус", 'status_str')
    )
