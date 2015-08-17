#coding: utf-8
from angular.field import TextFieldBootstrap, BehaviorHiddenPredicate
from angular.fieldview import FieldWidget, TableLocalWidgetCondition
from angular.urls import ResourceAngularUrl, ResourceAngularInnerUrl, ResourceGetAngularUrl
from angular.view import ModelProjectAngularView

from applications.good.views import GoodViewAngular
from applications.inventory.constant import COUNT_BEFORE_ATTR, COUNT_AFTER_ATTR
from applications.inventory.extra import ExtraInventoryStatus, InventoryStatusExtra
from applications.inventory.resource import InventoryCanon, InventoryItemCanon, InventoryItemInnerCanon, InventoryPrint
from applications.inventory.models import Inventory, InventoryItems
from applications.point_sale.views import PointSaleAngularView


class InventoryItemView(ModelProjectAngularView):
    """
    Базовый View для позиций товара в инвентаризации.
    """
    resource_view = ResourceAngularUrl('/api', '/inventory-items', InventoryItemCanon)
    model = InventoryItems

    dict_select_attr = 'good.full_name'

    columns = (
        (u"Товар", 'good.full_name_with_price'),
        (u"Кол-во до", COUNT_BEFORE_ATTR),
        (u"Кол-во после", COUNT_AFTER_ATTR)
    )

    form_columns = {
        'good': FieldWidget(
            col='good', label=u"Товар", view=GoodViewAngular()
        ),
        COUNT_BEFORE_ATTR: (u"Количество до", u""),
        COUNT_AFTER_ATTR: (u"Количество после", u"")
    }

    columns_local = (
        (u"Товар", 'good.full_name_with_price'),
        (u"Кол-во до", COUNT_BEFORE_ATTR),
        (u"Кол-во после", COUNT_AFTER_ATTR)
    )


#TODO архитектура кривовата(мне нужно создавать View только для ресурса).
class InventoryItemInnerView(InventoryItemView):
    """
    View для вложенных урлов.
    """
    resource_view = ResourceAngularInnerUrl("/api", "/inventory", InventoryItemInnerCanon)


class InventoryView(ExtraInventoryStatus, ModelProjectAngularView):
    """
    View для инвентаризации.
    """
    resource_view = ResourceAngularUrl('/api', '/inventory', InventoryCanon)
    resource_print = ResourceGetAngularUrl("/api", "/inventory/print", InventoryPrint)
    model = Inventory

    label_root = u"Инвентаризация"

    main_attrs = ('number', )

    dict_select_attr = 'number'

    extra = (InventoryStatusExtra(), )

    form_columns = {
        'number': TextFieldBootstrap(id='number', label=u"Номер ревизии", placeholder=u"Введите номер ревизии",
                                     required=True),
        'datetimenew': TextFieldBootstrap(id='datetimenew', label=u"Дата и время", filter="date:'d MMM y, HH:mm:ss'",
                                       behaviors=[BehaviorHiddenPredicate('model.id == undefined || editMode'), ]),
        'location': FieldWidget(
            col='location', label=u"Торговая точка", view=PointSaleAngularView(), required=True,
            link="/admin/pointsaleangularview/")
    }

    tabs = (
        TableLocalWidgetCondition(
            title=u"Продукты", view=InventoryItemInnerView(), attr="items"),
    )

    columns = (
        (u'Номер', 'number'),
        (u"Торговая точка", 'location_name'),
        (u"Дата и время начала", 'datetimenew', "date:'d MMM y, HH:mm:ss' : timezone"),
        (u'Статус', 'status_str'),
    )