#coding: utf-8
from flask import render_template
from angular.view import ExtraMixinView, ExtraStatus
# from applications.acceptance.model import DRAFT, IN_PROG, VALIDATED
from applications.return_app.model import DRAFT, IN_PROG, IN_DEL, FINISH


class ExtraReturnStatus(ExtraMixinView):
    def page_to_index(self):
        return "test/extra/return/reestr-extra.html"


class ReturnStatusExtra(ExtraStatus):
    url = "/api/return/:id/status"

    def view_header(self):
        return render_template("test/extra/return/header.html")

    def create_js(self):
        return render_template(
            "test/extra/return/create.js",
            name=self.get_name())

    def edit_js(self):
        return render_template(
            "test/extra/return/edit.js",
            name=self.get_name(), status=FINISH)

    def edit_js_instance(self):
        return render_template(
            "test/extra/return/edit-instance.js",
            status_1=DRAFT,
            status_2=IN_PROG,
            status_3=IN_DEL)

    def edit_btn(self):
        return render_template(
            "test/extra/return/edit-btn.js",
            status_1=DRAFT,
            status_2=IN_PROG,
            status_3=IN_DEL)