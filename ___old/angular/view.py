#coding: utf-8\n__author__ = 'StasEvseev'
from flask import render_template, request, g
from flask.ext.admin.base import AdminViewMeta, expose, BaseView
from werkzeug.utils import redirect
from flask.ext import login

from old.angular.fieldview.table import Table
from log import error, debug
from tools import pathrend_to_cache
from tools.cache import save_page_to_cache


class AngularMeta(AdminViewMeta):
    def __init__(cls, classname, bases, fields):
        super(AngularMeta, cls).__init__(classname, bases, fields)

        for p in dir(cls):
            if p == 'index':
                @expose('/<path:path>')
                def ind(self, *args, **kwargs):
                    return self.index()
                cls.ind = ind


class AngularView(BaseView):
    """
    Базовый класс для выюшек ангуляра.
    Всего один метод view - index - ловит все субурлы и передает ему.
    """
    __metaclass__ = AngularMeta

    @expose('/')
    def index(self):
        pass


class ProjectAngularView(AngularView):

    def get_id(self):
        return self.__class__.__name__.lower()

    def is_accessible(self):
        return login.current_user.is_authenticated()

    def inaccessible_callback(self, name, **kwargs):
        return

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect('/?target=%s' % request.path)
        g.user = login.current_user
        return self.index_view()

    def index_view(self):
        pass


class ModalWidget(object):

    def __init__(self, widget):
        self.widget = widget
        self.view = widget.view

    def modal_id(self):
        return self.widget.modal_id()

    def render(self):
        res = self.widget.render()
        if res is None:
            return render_template("test/modals/window.html",
                                   modal_id=self.modal_id(),
                                   form=self.view.get_form(),
                                   label_new=self.view.label_modal_new or "",
                                   label_edit=self.view.label_modal_edit or "",
                                   label_model="",
                                   btn_ok=u"Сохранить" or "",
                                   btn_ok_edit=u"Сохранить" or "",
                                   btn_cancel=u"Отменить" or "")
        else:
            return res

    def render_resource(self):
        res = self.widget.render_resource()
        if res is None:
            url_create, url_update, url_delete, url_get, url_getall = self.view.get_urls()
            table_res = " ".join([x.render_res() for x in self.view.form_tables])
            return render_template("test/modals/resource.js",
                                   modal_cntr=self.widget.modal_cntr(),
                                   url_create=url_create,
                                   url_update=url_update,
                                   url_delete=url_delete,
                                   url_get=url_get,
                                   url_getall=url_getall,
                                   table_res=table_res)
        else:
            return res

    def render_controller(self):
        res = self.widget.render_controller()
        if res is None:
            return render_template("test/modals/controller.js",
                                   modal_cntr=self.widget.modal_cntr(),
                                   modals=self.view._get_extra(),
                                   form=self.view.get_form())
        else:
            return res


class ModelProjectAngularView(ProjectAngularView):
    """
    View по модели.

    Может также участвовать в качестве поля dictSelectField.
    """
    #Ресурс к REST_API
    resource_view = None
    resource_print = None
    #Шаблон для отображения
    page = "test/reestr.html"
    #Модель SQLAlchemy
    model = None
    """
    Формовые поля
    """
    form_columns = {}
    """
    Колонки в табличном представлении.
    Структура:
    ...
        ("Заголовок столбца", "Аттрибут модели из @resource_view:get", "Фильтр ангуляра(необязателен)"),
    ...
    """
    columns = (

    )
    """
    Колонки в таблицу локального редактирования
    """
    columns_local = (

    )
    """
    Колонки в таблицу с редактирование без модального окна
    """
    columns_edit_inline = (

    )

    """
    Представления другой модели в tabs
    """
    tabs = ()

    form_tables = ()

    """
    Кастомизация отображения slave полей на форме.
    Особенность - стобцов должно быть (1, 2, 3, 4, 6, 12).
    """
    grouping = ()
    EMPTY_COL = ('', ())

    """
    Аттрибут, который будет высвечиваться в breadcrumbs
    """
    bread_attr = ''

    dict_select_attr = 'tostring'

    """
    Аттрибуты, что будут особо выражены на форме
    """
    main_attrs = ()
    """
    Лэйбл в представление 'Список -> Элемент_1 -> Редактирование'
    """
    label_root = u"Список"
    """
    Лэйблы в модальное окно
    """
    label_modal_new = u"Создание"
    label_modal_edit = u"Открыто"

    global_var = {

    }

    prefix_admin = "/admin"

    can_search = True
    can_create = True
    can_delete = True
    can_update = True
    #CACHING
    _cache = None

    def get_form(self):
        from old.angular.form import Form
        try:
            debug(u"Создание формы для %s." % self.model)
            form = Form(self.model).create_form(self.form_columns, self.main_attrs, self.grouping)
            form.set_form_tables(self.form_tables)
            return form
        except Exception as exc:
            error(unicode(exc))
            raise
        finally:
            debug(u"Создание формы для %s завершенно." % self.model)

    def page_to_index(self):
        return self.page

    def table(self, main=False, ms=False, counts=None, resource=None, selectable=True, select_func="select"):
        #Тут собираем колонки в таблицу
        # columns = []
        # for col in self.columns:
        #     if len(col) == 2:
        #         res = (col[0], col[1], "", (None, None))
        #     elif len(col) == 3:
        #         res = (col[0], col[1], col[2], (None, None))
        #     else:
        #         res = (col[0], col[1], col[2], col[3])
        #     columns.append(res)

        columns = [(x[0], x[1], "") if len(x) == 2 else (x[0], x[1], x[2]) for x in self.columns]
        table = Table(columns, main, ms, counts, resource, selectable, select_func)
        return table

    def args_to_index(self):
        #собираем модальные окна
        modals = self._collect_modals()
        form = self.get_form()
        url_create, url_update, url_delete, url_get, url_getall = self.get_urls()
        table = self.table(main=True)

        arg = {
            'form': form,
            'tabs': self.tabs,
            'modals': self._get_extra(),
            'modals_window': modals,
            'label_root': self.label_root,
            'main_attr': self.bread_attr if self.bread_attr else self.main_attrs[0] if self.main_attrs else '',
            'can_search': self.can_search,
            'can_create': self.can_create,
            'can_delete': self.can_delete,
            'can_update': self.can_update,
            'table': table,
            'url_view': self.get_url_view(),
            'url_create': url_create,
            'url_update': url_update,
            'url_delete': url_delete,
            'url_get': url_get,
            'url_getall': url_getall,
            'url_to_print': self.resource_print.url_get() if self.resource_print else None
            # 'token': login.current_user.generate_auth_token()
        }
        return arg

    def __index_view(self):
        try:
            debug(u"Генерируем страницу для %s." % self.__class__.__name__)
            page = self.render(self.page_to_index(),
                               **self.args_to_index())
        except Exception as exc:
            error(unicode(exc))
            debug(u"Генерирование страницы для %s не удалось." % self.__class__.__name__)
            raise
        else:
            debug(u"Генерирование страницы для %s завершенно." % self.__class__.__name__)
            return page

    def get_urls(self):
        return (self.resource_view.url_create(), self.resource_view.url_update(), self.resource_view.url_delete(),
                self.resource_view.url_get(), self.resource_view.url_getall())

    def get_url_view(self):
        return "".join([self.prefix_admin, '/', self.__class__.__name__.lower()])

    #TODO Start. Поведение для dictSelectField'а вынести в миксин хотя бы.
    def _get_extra(self):
        from .old.angular.fieldview import FieldWidget
        return [x for x in self.form_columns.values() if isinstance(x, FieldWidget)]

    def modal_id(self):
        return self.__class__.__name__.lower()

    def index_modal(self, label_model, label_modal_new=None, label_modal_edit=None, btn_ok=None, btn_ok_edit=None,
                    btn_cancel=None):
        try:
            return render_template("test/modal/modal.html", form=self.get_form(),
                                   label_new=self.label_modal_new or label_modal_new,
                                   label_edit=self.label_modal_edit or label_modal_edit,
                                   label_model=label_model,
                                   btn_ok=u"Сохранить" or btn_ok,
                                   btn_ok_edit=u"Сохранить" or btn_ok_edit,
                                   btn_cancel=u"Отменить" or btn_cancel)
        except Exception as exc:
            error(unicode(exc))
            raise
    #TODO End.

    def _collect_globals(self):
        res = ""
        for k, v in self.global_var.iteritems():
            res += ("$rootScope." + str(k) + " = " + str(v()) + "; ")
        for n, extra in self._get_all_extra().iteritems():
            for k, v in extra.view.global_var.iteritems():
                res += ("$rootScope." + str(k) + " = " + str(v()) + "; ")
        return res

    #CACHING
    def index_view(self):
        def f():
            debug(u"Берем страницу из кэша для %s." % self.__class__.__name__)
            return self.render(pathrend_to_cache(self.__class__.__name__),
                               token=login.current_user.generate_auth_token(),
                               globals=self._collect_globals())
        # debug(u"Проверяем кэш на наличие страницы для %s." % self.__class__.__name__)
        if self._cache is None:
            result = self.__index_view()
            save_page_to_cache(result, self.__class__.__name__)
            debug(u"Сохраняем в кэш страницу %s." % self.__class__.__name__)
            self._cache = True
        return f()

    def _collect_modals(self):
        modals = []
        extra = self._get_all_extra()

        for ext in extra.keys():
            modals.append(ModalWidget(extra[ext]))
        return modals

    def _get_all_extra(self):
        res = {}

        def rec(view):
            extra = view._get_extra()
            tabs = view.tabs
            for f in extra:
                res[f.modal_cntr()] = f
                rec(f.view)
            for t in tabs:
                res[t.modal_cntr()] = t
                rec(t.view)
        rec(self)
        return res


class ExtraMixinView(object):
    extra = ()

    def page_to_index(self):
        return "test/reestr-extra.html"

    def args_to_index(self):
        args = super(ExtraMixinView, self).args_to_index()
        args['extra'] = self.extra
        return args


class Extra(object):

    pass


class ExtraStatus(Extra):

    url = None

    def view_header(self):
        return ""

    def dependency(self):
        return self.get_name() + "RES_STATUS"

    def create_js(self):
        return ""

    def edit_js(self):
        return ""

    def edit_js_instance(self):
        return ""

    def edit_btn(self):
        return ""

    def resources(self):
        return render_template(
            "test/extra/status/resource.js",
            name=self.get_name(), url=self.url)

    def get_name(self):
        return self.__class__.__name__.lower()