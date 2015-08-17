#coding: utf-8
from angular.field import DateFieldBootstrap
from angular.fieldview import FieldWidget, TableLocalW
from angular.urls import ResourceAngularInnerUrl, ResourceAngularUrl
from angular.view import ModelProjectAngularView

from applications.provider_app.views import ProviderAngularView
from applications.return_app import ReturnCanon, ReturnItemInnerCanon
from applications.return_app.extra import ExtraReturnStatus, ReturnStatusExtra
from applications.return_app.model import ReturnItem, Return


class ReturnItemView(ModelProjectAngularView):
    resource_view = ResourceAngularInnerUrl("/api", "/return", ReturnItemInnerCanon)
    model = ReturnItem

    columns_edit_inline = (
        (u"Наименование", 'full_name', (TableLocalW.OTHER, None, None)),
        (u"Цена с НДС", 'price_with_NDS', (TableLocalW.OTHER, 'rub', None)),
        (u"К. зак.", 'count_delivery', (TableLocalW.OTHER, None, None)),
        (u"К. рем.", 'count_rem', (TableLocalW.OTHER, None, None)),
        (u"Кол-во", 'count', (TableLocalW.NUNMER_COL, None, None)),
    )


class ReturnView(ExtraReturnStatus, ModelProjectAngularView):
    resource_view = ResourceAngularUrl("/api", "/return", ReturnCanon)
    model = Return

    dict_select_attr = 'name'

    # can_create = False

    columns = (
        (u"Дата отправки", 'date', "date:'d MMM y'"),
        (u"Поставшик", 'provider.name'),
        (u"Дата от", 'date_start', "date:'d MMM y'"),
        (u"Дата до", 'date_end', "date:'d MMM y'")
    )

    bread_attr = 'provider.name'

    main_attrs = ('provider',)

    form_columns = {
        'provider': FieldWidget(col='provider', label=u"Поставщик", view=ProviderAngularView(),
                                required=True),
        # 'date_start': DateFieldBootstrap(id="date_start", label=u"Дата от", required=True),
        # 'date_end': DateFieldBootstrap(id='date_end', label=u"Дата до", required=True),
    }

    extra = (
        ReturnStatusExtra(),
    )

    # grouping = (
    #     (
    #         (u'Даты возврата', ('date_start', 'date_end')),
    #     ),
    # )

    tabs = (
        TableLocalW(
            title=u"Продукты", view=ReturnItemView(), attr="items", remove=False),
    )