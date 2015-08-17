#coding: utf-8
from flask import render_template
from angular.view import ExtraMixinView, ExtraStatus
from applications.waybill.models import DRAFT, IN_PROG, IN_DELIVERY, FINISH


class ExtraWayBillStatus(ExtraMixinView):
    
    def page_to_index(self):
        return "test/extra/waybill/reestr-extra.html"


class WaybillStatusExtra(ExtraStatus):
    url = "/api/waybill/:id/status"

    def view_header(self):
        return render_template("test/extra/waybill/waybill-header.html")

    def create_js(self):
        return render_template(
            "test/extra/waybill/create.js",
            name=self.get_name())

    def edit_js(self):
        return render_template(
            "test/extra/waybill/edit.js",
            name=self.get_name(), status=FINISH)

    def edit_js_instance(self):
        return render_template(
            "test/extra/waybill/edit-instance.js",
            status_1=DRAFT,
            status_2=IN_PROG,
            status_3=IN_DELIVERY,
            status_4=FINISH)

    def edit_btn(self):
        return render_template(
            "test/extra/waybill/edit-btn.js",
            status_1=DRAFT,
            status_2=IN_PROG,
            status_3=IN_DELIVERY,
            status_4=FINISH)