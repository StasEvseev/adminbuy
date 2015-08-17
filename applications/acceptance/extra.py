#coding: utf-8
from flask import render_template
from angular.view import ExtraMixinView, ExtraStatus
from applications.acceptance.model import DRAFT, IN_PROG, VALIDATED


class ExtraAcceptanceStatus(ExtraMixinView):
    def page_to_index(self):
        return "test/extra/acceptance/reestr-extra.html"


class AcceptanceStatusExtra(ExtraStatus):
    url = "/api/acceptance/:id/status"

    def view_header(self):
        return render_template("test/extra/acceptance/header.html")

    def create_js(self):
        return render_template(
            "test/extra/acceptance/create.js",
            name=self.get_name())

    def edit_js(self):
        return render_template(
            "test/extra/acceptance/edit.js",
            name=self.get_name(), status=VALIDATED)

    def edit_js_instance(self):
        return render_template(
            "test/extra/acceptance/edit-instance.js",
            status_1=DRAFT,
            status_2=IN_PROG,
            status_3=VALIDATED)

    def edit_btn(self):
        return render_template(
            "test/extra/acceptance/edit-btn.js",
            status_1=DRAFT,
            status_2=IN_PROG,
            status_3=VALIDATED)