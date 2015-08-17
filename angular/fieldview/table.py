#coding: utf-8
from flask import render_template


class Table(object):
    def __init__(self, list_columns, main=False, ms=False, counts=None, resource=None, selectable=True, select_func="select"):
        self.list_columns = list_columns
        self.ms = ms
        self.counts = counts
        self.resource = resource
        self.selectable = selectable
        self.select_func = select_func
        self.main = main

    def render(self):
        return render_template("test/view/table.html", list_columns=self.list_columns, ms=self.ms,
                               counts=self.counts, resource=self.resource or "resource",
                               select_func=self.select_func,
                               selectable=self.selectable, main=self.main)


class Column(object):
    def __init__(self, label, attr, filter=None, extra=None):
        self.label = label
        self.attr = attr
        self.attr_cl = attr.replace(".", "_")
        self.filter = filter
        self.extra = extra

    def render_th(self):
        return u"""<th %s>%s</th>""" % (self.extra, self.label)

    def render_td(self):
        return u"""<td %s class="%s"><span>[[ item.%s %s ]]</span></td>""" % (
            self.extra,
            self.attr_cl,
            self.attr,
            self._filter())

    def _filter(self):
        return u"| %s" % self.filter if self.filter else u""


class NumberColumn(Column):
    def render_td(self):
        return u"""
        <td %s class="%s">
            <div ng-show="editMode">
                <input nks-only-number ng-model="item.%s" ng-change="item.count_change()" class="input-small input-table-sm"
                   type="text" placeholder="Количество"/>
            </div>
            <div ng-hide="editMode">
                [[item.%s %s]]
            </div>
        </td>
        """ % (self.extra, self.attr_cl, self.attr, self.attr, self._filter())


class NumberColumnStatus(Column):
    """
    Номерная колонка со статусом(перестает быть редактируемой в некоторых статусах).
    """
    def __init__(self, label, attr, filter=None, extra=None, status=None):
        super(NumberColumnStatus, self).__init__(label, attr, filter, extra)
        self.status = status

    @classmethod
    def from_numbercolumn(cls, column, status):
        return NumberColumnStatus(
            label=column.label, attr=column.attr, filter=column.filter, extra=column.extra, status=status)

    def render_td(self):
        return u"""
        <td %s class="%s">
            <div ng-show="editMode && model.status!=%s">
                <input nks-only-number ng-model="item.%s" ng-change="item.count_change()" class="input-small input-table-sm"
                   type="text" placeholder="Количество"/>
            </div>
            <div ng-hide="editMode && model.status!=%s">
                [[item.%s %s]]
            </div>
        </td>
        """ % (self.extra, self.attr_cl, self.status, self.attr, self.status, self.attr, self._filter())


class NumberColumnStatuses(Column):
    """
    Номерная колонка со статусом(перестает быть редактируемой в некоторых статусах).
    """
    def __init__(self, label, attr, filter=None, extra=None, statuses=None):
        super(NumberColumnStatuses, self).__init__(label, attr, filter, extra)
        self.statuses = statuses

    @classmethod
    def from_numbercolumn(cls, column, statuses):
        return NumberColumnStatuses(
            label=column.label, attr=column.attr, filter=column.filter, extra=column.extra, statuses=statuses)

    def render_td(self):
        return u"""
        <td %s class="%s">
            <div ng-show="editMode && %s">
                <input nks-only-number ng-model="item.%s" ng-change="item.count_change()" class="input-small input-table-sm"
                   type="text" placeholder="Количество"/>
            </div>
            <div ng-hide="editMode && %s">
                [[item.%s %s]]
            </div>
        </td>
        """ % (
            self.extra,
            self.attr_cl,
            u"(" + u"&&".join([u"model.status!=" + unicode(x) for x in self.statuses]) + u")",
            self.attr,
            u"(" + u"&&".join([u"model.status!=" + unicode(x) for x in self.statuses]) + u")",
            self.attr,
            self._filter()
        )


class CalculateColumn(Column):

    def __init__(self, label, attr, filter=None, extra=None, expr=None):
        super(CalculateColumn, self).__init__(label, attr, filter, extra)
        self.expr = expr

    def render_td(self):
        return u"""
        <td %s class="%s">
            [[ %s %s ]]
        </td>
        """ % (self.extra, self.attr_cl, self.expr, self._filter())