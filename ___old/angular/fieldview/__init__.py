#coding: utf-8\n__author__ = 'StasEvseev'
from flask import render_template

from angular.field import DictSelectField
from old.angular.fieldview.table import NumberColumn, CalculateColumn, Column, NumberColumnStatus


class Widget(object):

    def __init__(self, view):
        self.view = view

    def modal_id(self):
        """
        Идентификатор модального окна
        """
        return "modal_id" + self.view.modal_id()

    def modal_cntr(self):
        """
        Контроллер для модального окна
        """
        return "modal_cntr" + self.__class__.__name__.lower() + self.view.__class__.__name__.lower()

    def render_resource(self):
        pass

    def render_controller(self):
        pass

    def render(self):
        pass


class FieldWidget(Widget):
    def __init__(self, col, label, view, placeholder=u"Выберите или поищите...", required=False, behaviors=None,
                 validators=None, link=None, can_create=True, can_edit=True):
        super(FieldWidget, self).__init__(view)
        self.label = label
        self.placeholder = placeholder
        self.col = col
        self.required = required
        self.behaviors = behaviors or []
        self.validators = validators or []
        self.link = link
        self.can_create = can_create
        self.can_edit = can_edit

    def field(self, is_main=False):
        return DictSelectField(
            id=self.col, label=self.label, placeholder=self.placeholder, modal_cntr=self.modal_cntr(),
            modal_id=self.modal_id(), tostring=self.view.dict_select_attr, is_main=is_main, required=self.required,
            behaviors=self.behaviors, validators=self.validators, link=self.link, can_create=self.can_create,
            can_edit=self.can_edit)

    #===================================================================================================================
    def depend_js_getall(self):
        return self.modal_cntr() + "RES_GETALL"

    def depend_js_get(self):
        return self.modal_cntr() + "RES_GET"

    def add_to_js(self):
        return " $scope.%s = %s" % (self.col, self.depend_js_getall() + ".meth")

    def set_value(self):
        ids = self.col + "_id"
        field = self.field()
        return """ if (data.%s) {%s.meth({id: data.%s}, function(res) {$scope.%s = res;}, function(res) {})} """ % (
            ids, self.depend_js_get(), ids, field.prefix + "." + field.id)

    def index_modal(self):
        return self.view.index_modal(self.label)


class TabWidget(Widget):
    def __init__(self, title, view, attr):
        super(TabWidget, self).__init__(view)
        self.attr = attr
        self.title = title

    def tab_id(self):
        """
        Идентификатор tab'а
        """
        return "tab_id" + self.view.__class__.__name__.lower()

    def render_table(self):
        """
        Рендеринг таблицы в Табы.
        """
        pass

    def depend(self):
        """
        Зависимости в контроллеры(Create и Edit).
        """
        pass

    def create_js(self):
        """
        Добавление параметров в scope CreateController.
        """
        pass

    def edit_js(self):
        """
        Добавление параметров в scope EditController.
        """
        pass

    def param_save(self):
        """
        Добавление параметров в сохранение Create и Edit.
        """
        pass

    def cond_hide(self):
        """
        Условие скрытности таба
        """
        pass

    def set_value(self):
        return ""


class TableLocalViewWidget(TabWidget):

    def __init__(self, title, view, attr, attr_id=None, search=False, redir=None):
        super(TableLocalViewWidget, self).__init__(title, view, attr)
        self.attr_id = attr_id or "id"
        self.search = search
        self.redir = redir

    def resource_table(self):
        return self.__class__.__name__ + self.view.__class__.__name__

    def render_table(self):
        kwargs = {}
        kwargs['resource'] = self.resource_table()
        if self.redir:
            kwargs['select_func'] = "select" + self.resource_table()

        return render_template("test/tabs/tables/table-local-view/table.html",
                               table=self.view.table(**kwargs), search=self.search)

    def param_save(self):
        return ""

    def depend(self):
        return self.tab_id() + "RES_GET"

    def create_js(self):
        return """
        """

    def edit_js(self):
        if self.redir:
            redir = """$scope.%s = function(obj) {
                location.href = %s;
                console.log("YES");
            }""" % ("select" + self.resource_table(), self.redir)
        else:
            redir = ""
        return """
            $scope.%(resource_table)s = {'id': $routeParams.id};
            $scope."""  % {
            'resource_table': self.resource_table()
        } + self.resource_table() + """ = function(param, callb){
            param['""" + self.attr_id + """'] = $routeParams.id;
        """ + self.depend() + """.meth(param, callb);
            }

        %s
        """ % redir

    def render_resource(self):
        return render_template("test/tabs/tables/table-local-view/resource.js",
                               table_id=self.tab_id(), url_get=self.view.get_urls())


class TableLocalWidget(TabWidget):
    """
    Представление View в таблице, хранящаяся на стороне клиента.
    """

    def columns(self):
        return [(x[0], x[1], "") if len(x) == 2 else (x[0], x[1], x[2]) for x in self.view.columns_local]

    def render_table(self):
        return render_template("test/tabs/tables/table.html",
                               columns_local=self.columns(), tab_id=self.tab_id())

    def render_controller(self):
        return render_template("test/modal/controller-local.js",
                               form=self.view.get_form(),
                               modal_cntr=self.modal_cntr(),
                               modals=self.view._get_extra())

    def depend(self):
        return self.modal_cntr() + "RES_GETALL" + "," + self.modal_cntr() + "RES_GET"

    def param_save(self):
        return render_template("test/tabs/tables/tablelocal_add_to_save.js", attr=self.attr, tab_id=self.tab_id())

    def create_js(self):
        return render_template("test/tabs/tables/tablelocal_add_to_js.js",
                               tab_id=self.tab_id(),
                               modal_id=self.modal_id(), modal_ctrl=self.modal_cntr())

    def set_value(self):
        return render_template("test/tabs/tables/tablelocal_set_value.js",
                               tab_id=self.tab_id(), hidden=self.cond_hide(),
                               modal_id=self.modal_id(), modal_ctrl=self.modal_cntr())

    def edit_js(self):
        return render_template("test/tabs/tables/tablelocal_add_to_js.js",
                               tab_id=self.tab_id(), hidden=self.cond_hide(),
                               modal_id=self.modal_id(), modal_ctrl=self.modal_cntr())


class TableLocalW(TabWidget):
    """
    Таблица на View с инлайн редактированием записей(без модального окна). С возможностями импорта из других реестров.
    """
    NUNMER_COL, CALC_COL, OTHER = "n", "calc", ""

    def __init__(self, title, view, attr, imports=None, remove=True):
        super(TableLocalW, self).__init__(title, view, attr)

        self.remove = remove

        self.imports = imports or []
        for imp in self.imports:
            imp.set_tab_id(self.tab_id())

    def _number_column(self, l, at, p, a):
        return NumberColumn(l, at, p, a)

    def _collect_columns(self):
        cols = []

        for col in self.view.columns_edit_inline:
            try:
                l, at, t = col
                t, f, a = t
                if t == TableLocalW.NUNMER_COL:
                    cols.append(self._number_column(l, at, None, a))
                elif t == TableLocalW.CALC_COL:
                    f, expr = f
                    cols.append(CalculateColumn(l, at, f, a, expr))
                else:
                    cols.append(Column(l, at, f, a))
            except Exception as exc:
                l, at = col
                cols.append(Column(l, at))
        return cols

    def render_table(self):
        cols = self._collect_columns()
        return render_template("test/tabs/tables/table-ms-edt/table.html",
                               columns_local=cols, tab_id=self.tab_id(), imports=self.imports, remove=self.remove)

    def render(self):
        return render_template("test/tabs/tables/table-ms-edt/imports_template.html", imports=self.imports)

    def render_controller(self):
        return render_template("test/tabs/tables/table-ms-edt/imports_controller.js",
                               imports=self.imports)

    def render_resource(self):
        url_create, url_update, url_delete, url_get, url_getall = self.view.get_urls()
        modal_cntr = self.modal_cntr()
        return render_template("test/tabs/tables/table-ms-edt/imports_resource.js",
                               imports=self.imports,
                               modal_cntr=modal_cntr,
                               url_create=url_create,
                               url_update=url_update,
                               url_delete=url_delete,
                               url_get=url_get,
                               url_getall=url_getall)

    def depend(self):
        return self.modal_cntr() + "RES_GETALL" + "," + self.modal_cntr() + "RES_GET"

    def param_save(self):
        return render_template("test/tabs/tables/tablelocal_add_to_save.js",
                               attr=self.attr,
                               tab_id=self.tab_id())

    def create_js(self):
        return render_template("test/tabs/tables/table-ms-edt/table-ms-atj.js",
                               tab_id=self.tab_id(),
                               imports=self.imports)

    def edit_js(self):
        return render_template("test/tabs/tables/table-ms-edt/table-ms-atj-edt.js",
                               tab_id=self.tab_id(),
                               imports=self.imports,
                               modal_ctrl=self.modal_cntr())


class TableLocalWidgetCondition(TableLocalWidget):

    def render_table(self):
        return render_template("test/tabs/tables/table-condition/table-local/table-condition.html",
                               columns_local=self.columns(), tab_id=self.tab_id())

    def edit_js(self):
        return render_template("test/tabs/tables/table-condition/table-local/table-condition_local_add_to_js_edit.js",
                               tab_id=self.tab_id(), hidden=self.cond_hide(),
                               modal_id=self.modal_id(), modal_ctrl=self.modal_cntr())