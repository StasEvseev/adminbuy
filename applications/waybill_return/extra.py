#coding: utf-8
from flask import render_template
from angular.view import ExtraMixinView, ExtraStatus
from applications.waybill_return.model import DRAFT, IN_PROG, IN_DELIVERY, IN_POINT, IN_CALC, FINISH


class ExtraWayBillReturnStatus(ExtraMixinView):
    
    def page_to_index(self):
        return "test/extra/waybill_return/reestr-extra.html"


class WaybillReturnStatusExtra(ExtraStatus):
    url = "/api/waybillreturn/:id/status"

    def view_header(self):
        return render_template("test/extra/waybill_return/waybill-header.html")

    def create_js(self):
        return render_template(
            "test/extra/waybill_return/create.js",
            name=self.get_name())

    def edit_js(self):
        return render_template(
            "test/extra/waybill_return/edit.js",
            name=self.get_name(), status=FINISH)

    def edit_js_instance(self):
        return render_template(
            "test/extra/waybill_return/edit-instance.js",
            status_1=DRAFT,
            status_2=IN_PROG,
            status_3=IN_DELIVERY,
            status_4=IN_POINT,
            status_5=IN_CALC,
            status_6=FINISH)

    def edit_btn(self):
        return render_template(
            "test/extra/waybill_return/edit-btn.js",
            status_1=DRAFT,
            status_2=IN_PROG,
            status_3=IN_DELIVERY,
            status_4=IN_POINT,
            status_5=IN_CALC,
            status_6=FINISH)