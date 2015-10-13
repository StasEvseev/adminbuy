#coding: utf-8

__author__ = 'StasEvseev'

# from flask import render_template
#
# from old.angular.fieldview import TableLocalW, NumberColumn
#
#
# # from applications.waybill.models import FINISH, DRAFT
# from old.angular.fieldview.table import NumberColumnStatuses
# from applications.waybill_return.model import DRAFT, IN_PROG, IN_DELIVERY, FINISH
#
#
# class TableLocalImportsCondWayRet(TableLocalW):
#     def _number_column(self, l, at, p, a):
#         return NumberColumnStatuses.from_numbercolumn(NumberColumn(l, at, p, a), [
#             DRAFT, IN_PROG, IN_DELIVERY, FINISH])
#
#     def render_table(self):
#         cols = self._collect_columns()
#         return render_template("test/tabs/tables/table-condition/table-local-import/table-condition.html",
#                                columns_local=cols, tab_id=self.tab_id(), imports=self.imports,
#                                status_1=DRAFT, status_2=FINISH, remove=self.remove)