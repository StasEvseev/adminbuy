#coding: utf-8

__author__ = 'StasEvseev'

from old.admin.core import MyAdmin
from old.admin.view.mail import MailView
from old.admin.view.login import MyAdminIndexView

from applications.acceptance.view import AcceptanceNewView
from applications.collection.view import CollectAngularView
from applications.commodity.views import CommodityAngularView
from applications.good.views import GoodViewAngular
from applications.inventory.views import InventoryView
from applications.point_sale.views import PointSaleAngularView
from applications.provider_app.views import ProviderAngularView
from applications.receiver.view import ReceiverAngularView
from applications.return_app.view import ReturnView
from applications.seller.view import SellerAngularView
from applications.settings.view import SettingView
from applications.waybill.views import WayBillView
from applications.waybill_return.view import WayBillReturnView

admin = MyAdmin(name=u"Личный кабинет",
                index_view=MyAdminIndexView(name=u"Главная"),
                base_template='my_master.html')

admin.add_view(MailView(name=u'Почта', menu_icon_type='glyph', menu_icon_value='fa fa-envelope'))
admin.add_view(WayBillView(name=u"Накладные", menu_icon_type='glyph', menu_icon_value='fa fa-table'))
admin.add_view(WayBillReturnView(name=u"Накладные возврата", menu_icon_type='glyph', menu_icon_value='fa fa-reply'))
admin.add_view(AcceptanceNewView(name=u"Приемки товара", menu_icon_type='glyph', menu_icon_value='fa fa-cube'))
admin.add_view(ReceiverAngularView(name=u"Оптовики", menu_icon_type='glyph', menu_icon_value='fa fa-users'))
admin.add_view(SellerAngularView(name=u"Продавцы", menu_icon_type='glyph', menu_icon_value='fa fa-female'))
admin.add_view(CollectAngularView(name=u"Инкассация", menu_icon_type='glyph', menu_icon_value='fa fa-money'))
admin.add_view(CommodityAngularView(name=u"Номенклатура", menu_icon_type='glyph', menu_icon_value='fa fa-bars'))
admin.add_view(GoodViewAngular(name=u"Продукты", menu_icon_type='glyph', menu_icon_value='fa fa-cubes'))
admin.add_view(ProviderAngularView(name=u"Поставщики", menu_icon_type='glyph', menu_icon_value='fa fa-truck'))
admin.add_view(PointSaleAngularView(name=u"Торговые точки", menu_icon_type='glyph', menu_icon_value='fa fa-archive'))
admin.add_view(InventoryView(name=u"Инвентаризация", menu_icon_type='glyph', menu_icon_value='fa fa-check-square-o'))
# admin.add_view(OrderView(name=u"Заказы", menu_icon_type='glyph', menu_icon_value='fa fa-cart-arrow-down'))
admin.add_view(ReturnView(name=u"Возвраты", menu_icon_type='glyph', menu_icon_value='fa fa-reply-all'))
admin.add_view(SettingView(name=u"Настройки", menu_icon_type="glyph", menu_icon_value="fa fa-cogs"))