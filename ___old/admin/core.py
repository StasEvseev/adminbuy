#coding: utf-8

__author__ = 'StasEvseev'

from flask.ext.admin import Admin
from flask.ext.admin.menu import MenuView


class MyMenuView(MenuView):
    def __init__(self, name, id, view=None):
        super(MyMenuView, self).__init__(name, view)
        self.id = id

    def get_id(self):
        return self.id


class MyAdmin(Admin):
    def _add_view_to_menu(self, view):
        self._add_menu_item(MyMenuView(view.name, view.get_id(), view), view.category)