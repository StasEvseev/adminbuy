#coding: utf-8
from flask import render_template
from angular.field import DecimalFieldBootstrap
from angular.fieldview import FieldWidget, Widget
from angular.urls import ResourceAngularInnerUrl, ResourceAngularUrl
from angular.view import ModelProjectAngularView
from applications.good.views import GoodViewAngular
from applications.invoice import InvoiceItemInnerCanon, InvoiceCanon
from applications.invoice.resource import InvoiceItemAcceptanceInnerCanon
from applications.price.service import PriceService
from models.invoice import Invoice
from models.invoiceitem import InvoiceItem


class InvoiceView(ModelProjectAngularView):
    resource_view = ResourceAngularUrl("/api", "/invoice_canon", InvoiceCanon)
    model = Invoice

    dict_select_attr = 'fullname'


class InvoiceItemView(ModelProjectAngularView):
    resource_view = ResourceAngularInnerUrl("/api", "/invoice_canon", InvoiceItemInnerCanon)
    model = InvoiceItem

    dict_select_attr = 'good.full_name'

    columns = (
        (u"Наименование", 'good.full_name'),
        (u"Количество", 'count')
    )


class TableWidget(object):

    def render_res(self):
        return """
        app.factory("PriceHelper", function($resource, Base64) {
          return $resource("/api/price/getprice", {}, {
            get: { method: "GET", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
          });
        });
        """

    def depend_js(self):
        return "PriceHelper"

    def render(self):
        return render_template("test/form/form_table/recommendation_price.html")

    def render_js(self):
        return render_template("test/form/form_table/recommendation_price.js")


class InvoiceItemsAcceptanceView(InvoiceItemView):
    resource_view = ResourceAngularInnerUrl("/api", "/from_acceptance", InvoiceItemAcceptanceInnerCanon)

    columns_local = (
        (u"Наименование", 'good.full_name'),
        (u"Количество", 'fact_count'),
        (u"Цена с НДС", 'price_with_NDS', 'rub'),
        (u"Цена розн.", 'price_retail', 'rub'),
        (u"Цена опт.", 'price_gross', 'rub'),
    )

    form_columns = {
        'good': FieldWidget(
            col='good', label=u"Товар", view=GoodViewAngular(), required=True),
        'price_with_NDS': DecimalFieldBootstrap(id='price_with_NDS', label=u"Цена с НДС", required=True),
        'fact_count': DecimalFieldBootstrap(id='fact_count', label=u"Количество", required=True),
        'price_retail': DecimalFieldBootstrap(
            id='price_retail', label=u"Цена розничная", required=True, non_model=True,
            input_group=True, input_group_popup=u"Рекомендуемая цена розницы!",
            input_group_exp="model.price_with_NDS * RATE_RETAIL |rub"),
        'price_gross': DecimalFieldBootstrap(
            id='price_gross', label=u"Цена оптовая", required=True, non_model=True,
            input_group=True, input_group_popup=u"Рекомендуемая цена опта!",
            input_group_exp="model.price_with_NDS * RATE_GROSS |rub"),
    }

    global_var = {
        "RATE_RETAIL": PriceService.RATE_RETAIL,
        "RATE_GROSS": PriceService.RATE_GROSS
    }

    form_tables = (
        TableWidget(),
    )

    main_attrs = ('good', )

    grouping = (
        (
            (u"Цены", ('price_with_NDS', 'price_retail', 'price_gross',)),
            (u'Параметры', ('fact_count', ))
        ),
    )