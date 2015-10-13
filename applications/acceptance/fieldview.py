#coding: utf-8

__author__ = 'StasEvseev'

# from flask import render_template
#
# from old.angular.fieldview import TableLocalW, NumberColumnStatus, NumberColumn, TableLocalWidgetCondition
# from applications.acceptance.model import VALIDATED, DRAFT, MAIL, NEW
#
#
# class TableLocalImportsCondAcc(TableLocalW):
#     def _number_column(self, l, at, p, a):
#         return NumberColumnStatus.from_numbercolumn(NumberColumn(l, at, p, a), VALIDATED)
#
#     def cond_hide(self):
#         return "model.type == %s" % NEW
#
#     def render_table(self):
#         cols = self._collect_columns()
#         return render_template("test/tabs/tables/table-condition/table-local-import/table-condition.html",
#                                columns_local=cols, tab_id=self.tab_id(), imports=self.imports,
#                                status_1=DRAFT, status_2=VALIDATED, type=NEW)
#
#
# class TableLocalWidgetAcc(TableLocalWidgetCondition):
#     def cond_hide(self):
#         return "model.type == %s" % MAIL