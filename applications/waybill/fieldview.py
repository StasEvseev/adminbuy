#coding: utf-8
from flask import render_template
from angular.fieldview import TableLocalW, NumberColumnStatus, NumberColumn
from applications.waybill.models import FINISH, DRAFT


class TableLocalImportsCondWay(TableLocalW):
    def _number_column(self, l, at, p, a):
        return NumberColumnStatus.from_numbercolumn(NumberColumn(l, at, p, a), FINISH)

    def render_table(self):
        cols = self._collect_columns()
        return render_template("test/tabs/tables/table-condition/table-local-import/table-condition.html",
                               columns_local=cols, tab_id=self.tab_id(), imports=self.imports,
                               status_1=DRAFT, status_2=FINISH, remove=self.remove)