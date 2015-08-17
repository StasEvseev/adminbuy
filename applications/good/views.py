#coding: utf-8

from angular.field import DecimalFieldBootstrap
from angular.field.validator import RequiredPredicate
from angular.fieldview import FieldWidget, TableLocalViewWidget
from angular.urls import ResourceAngularUrl
from angular.view import ModelProjectAngularView

from applications.commodity.views import CommodityAngularView
from applications.good import GoodResourceCanon
from applications.good.model import Good
from applications.good_price.view import PriceToGoodView


class GoodViewAngular(ModelProjectAngularView):
    resource_view = ResourceAngularUrl('/api', '/good', GoodResourceCanon)
    model = Good

    main_attrs = ('commodity', )
    label_root = u"Товар"
    bread_attr = 'full_name'
    dict_select_attr = 'full_name'

    grouping = (
        (
            (u'Номера', ('number_local', 'number_global')),
            (u"Цены", ('price.price_retail', 'price.price_gross')),
        ),
    )

    #формовые поля
    form_columns = {
        'commodity': FieldWidget(
            col='commodity', label=u"Номенклатура", view=CommodityAngularView(), required=True,
            link="/admin/commodityangularview/"),
        'number_local': DecimalFieldBootstrap(
            id='number_local', label=u"№(годовой)", prefix="model", placeholder=u"Введите номер", validators=[
                RequiredPredicate('commodity.numeric',
                                  u"Для номерной номенклатуры обязательно заполнения поля '%s'",
                                  u"Для безномерной номенклатуры поле '%s' должно быть пустым.")]),
        'number_global': DecimalFieldBootstrap(
            id='number_global', label=u"№(общий)", prefix="model", placeholder=u"Введите номер", validators=[
                RequiredPredicate('commodity.numeric',
                                  u"Для номерной номенклатуры обязательно заполнения поля '%s'",
                                  u"Для безномерной номенклатуры поле '%s' должно быть пустым.")]),
        'price.price_retail': (u"Цена розницы", u""),
        'price.price_gross': (u"Цена опта", u"")
    }

    #колонки в табличном представлении
    columns = (
        (u"Полное наименование", 'full_name'),
        (u"Номер в пределах года", 'number_local'),
        (u"Номер в пределах издания", 'number_global'),
    )

    tabs = (
        TableLocalViewWidget(title=u"Цены прихода", view=PriceToGoodView(), attr='asd'),
    )