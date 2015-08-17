#coding: utf-8

from angular.field import TextFieldBootstrap, BooleanBootstrap
from angular.fieldview import TableLocalViewWidget
from angular.urls import ResourceAngularUrl
from angular.view import ModelProjectAngularView

from applications.commodity.models import Commodity
from applications.commodity.resource import CommodityCanonResource
from applications.good_commodity.view import GoodView
from applications.seller import SellerResource
from applications.seller.model import Seller


class SellerAngularView(ModelProjectAngularView):
    resource_view = ResourceAngularUrl("/api", "/seller", SellerResource)
    model = Seller

    label_root = u"Продавцы"

    main_attrs = ('fname', )

    dict_select_attr = 'fullname'

    bread_attr = 'fullname'

    form_columns = {'fname': TextFieldBootstrap(id="fname", label=u"Имя", placeholder=u"Введите имя", required=True),
                    'lname': (u"Фамилия", u"Введите фамилию"),
                    'pname': (u"Отчество", u"Введите отчество"),
                    'address': (u"Адрес", u""),
                    'passport': (u"Паспортные данные", u"")}

    grouping = (
        (
            (u"Личные данные", ('lname', 'pname')),
            (u"Юридическая информация", ('address', 'passport',))
        ),
    )

    columns = (
        (u'Полное имя', 'fullname'),
        (u'Адрес', 'address'),
        (u'Паспортные данные', 'passport')
    )
    #
    # tabs = (
    #     TableLocalViewWidget(view=GoodView(), attr="attrgoodlocal", title=u"Товары"),
    # )