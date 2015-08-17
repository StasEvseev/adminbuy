#coding: utf-8
from flask import render_template
from angular.view import ExtraMixinView, ExtraStatus
from applications.inventory.models import StatusType, DRAFT, IN_PROG, VALIDATED


class ExtraInventoryStatus(ExtraMixinView):

    def page_to_index(self):
        return "test/extra/inventory/reestr-extra.html"


class InventoryStatusExtra(ExtraStatus):
    """
    Добавляем кнопки перехода по статусам Инвентаризации.
    """
    url = "/api/inventory/:id/status"

    def view_header(self):
        return render_template("test/extra/inventory/inventory-status.html")

    def create_js(self):
        return render_template(
            "test/extra/inventory/inventory-status-create.js",
            name=self.get_name())

    def create_js_after(self):
        return ""

    def edit_js(self):
        return render_template(
            "test/extra/inventory/inventory-status-edit.js",
            name=self.get_name(), status=VALIDATED)

    def edit_js_instance(self):
        return render_template(
            "test/extra/inventory/inventory-status-edit-instance.js",
            status_1=DRAFT,
            status_2=IN_PROG,
            status_3=VALIDATED)

    def edit_btn(self):
        return render_template(
            "test/extra/inventory/inventory-status-edit-btn.js",
            status_1=DRAFT,
            status_2=IN_PROG,
            status_3=VALIDATED)