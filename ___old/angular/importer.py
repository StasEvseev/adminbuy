#coding: utf-8\n__author__ = 'StasEvseev'
from flask import render_template


class Importer(object):

    view = None
    label_modal = ""

    def set_tab_id(self, tab_id):
        self.tab_id = tab_id

    def render_to_parent_controller(self):
        return render_template("test/tabs/tables/import/to_controller.js",
                               import_id=self.import_id(),
                               tab_id=self.tab_id,
                               import_modal_id=self.import_modal_id(),
                               import_modal_ctrl=self.import_modal_ctrl())

    def render_template(self):
        return render_template("test/tabs/tables/import/modal.html",
                               modal_id=self.import_modal_id(), label=u"Выбор",
                               label_model=self.label_modal,
                               table=self.view.table(ms=True, counts=[10, 25, 50, 100, 250, 500]),
                               btn_ok=u"Выбрать", btn_cancel=u"Отмена")

    def render_controller(self):
        return render_template("test/tabs/tables/import/controller.js",
                               modal_cntr=self.import_modal_ctrl(),
                               res_get_all=self.res_get_all(),
                               depend=self.depend())

    def depend(self):
        return "," + self.import_id() + "RES_GETALL" + "," + self.import_id() + "RES_GET"

    def res_get_all(self):
        return self.import_id() + "RES_GETALL"

    def render_resource(self):
        url_create, url_update, url_delete, url_get, url_getall = self.view.get_urls()
        return render_template("test/tabs/tables/import/resource.js",
                               import_id=self.import_id(),
                               url_create=url_create,
                               url_update=url_update,
                               url_delete=url_delete,
                               url_get=url_get,
                               url_getall=url_getall)

    def label(self):
        pass

    def import_id(self):
        return self.__class__.__name__

    def import_modal_id(self):
        return "importmodal_" + self.import_id()

    def import_modal_ctrl(self):
        return "importmodal_" + self.import_id()