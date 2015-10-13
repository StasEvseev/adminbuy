#coding: utf-8

__author__ = 'StasEvseev'

# from flask import render_template
#
# from old.angular.fieldview import FieldWidget
# from angular.importer import Importer
# from applications.invoice.view import InvoiceItemView, InvoiceView
# from applications.point_sale.views import PointSaleItemView
#
#
# class ImporterFromPointSale(Importer):
#     view = PointSaleItemView()
#     label_modal = u"Позиции товарной точки"
#
#     def label(self):
#         return u"""Добавить из торговой точки"""
#
#
# class ImporterFromInvoice(Importer):
#     view = InvoiceItemView()
#     view_dict = InvoiceView()
#     widget = FieldWidget(
#         col='invoice', label=u"Накладная", view=view_dict, required=True)
#     label_modal = u"Позиции накладной"
#
#     def label(self):
#         return u"""Добавить из накладной прихода"""
#
#     def render_template(self):
#         return render_template("test/tabs/tables/import/invoice/modal.html",
#                                modal_id=self.import_modal_id(), label=u"Выбор",
#                                label_model=self.label_modal,
#                                dict_select=self.widget.field(),
#                                table=self.view.table(ms=True, counts=[10, 25, 50, 100, 250, 500]),
#                                btn_ok=u"Выбрать", btn_cancel=u"Отмена")
#
#     def render_controller(self):
#         return render_template("test/tabs/tables/import/invoice/controller.js",
#                                modal_cntr=self.import_modal_ctrl(),
#                                res_get_all=self.res_get_all(),
#                                res=self.widget.modal_cntr() + "RES_GETALL",
#                                dict='invoice',
#                                depend=self.depend())
#
#     def depend(self):
#         return "," + self.import_id() + "RES_GETALL" + "," + self.import_id() + "RES_GET" + "," + self.widget.modal_cntr() + "RES_GETALL"
#
#     #TODO ПЕРЕДЕЛАТЬ КОСТЫЛИ
#     def render_resource(self):
#         url_create, url_update, url_delete, url_get, url_getall = self.view.get_urls()
#         url_c, url_u, url_d, url_g, url_ga = self.view_dict.get_urls()
#         return render_template("test/tabs/tables/import/invoice/resource.js",
#                                import_id=self.import_id(),
#                                url_create=url_create,
#                                url_update=url_update,
#                                url_delete=url_delete,
#                                url_get=url_get,
#                                url_getall=url_getall,
#
#                                modal_cntr=self.widget.modal_cntr(),
#                                url_create_1=url_c,
#                                url_update_1=url_u,
#                                url_delete_1=url_d,
#                                url_get_1=url_g,
#                                url_getall_1=url_ga,
#                                )