#coding: utf-8\n__author__ = 'StasEvseev'
from flask import render_template
from log import error


class FormBootstrap(object):

    def __init__(self):
        self.fld_map = {}
        self.fields = []
        #группировка полей
        #Весь вывод можно поделить на участки
        #структура:
        # элементы tuple - это строки
        # элементы строк - это столбцы. Их структура следующая ('Имя группы', (fields, ...))
        # (
        #   (), - строки
        #   (
        #       ('...', (field1, field2, ..., fieldN))
        #   )
        # )
        self.grouping = ()
        self.form_tables = ()

    def add_field(self, field):
        id = field.id
        self.fld_map[id] = field
        self.fields.append(field)

    def set_group(self, group):
        self.grouping = group

    def set_form_tables(self, form_tables):
        self.form_tables = form_tables

    def form_tables_render(self):
        try:
            return " ".join([x.render() for x in self.form_tables])
        except Exception as exc:
            error(unicode(exc))
            raise

    def render(self):
        try:
            self.fields.sort(key=lambda x: x.is_main)
            slaves = filter(lambda x: x.is_main is False, self.fields)
            mains = filter(lambda x: x.is_main, self.fields)
            if mains:
                mains[0].main = True
            if not self.grouping:
                grouping = (
                    (
                        ('', slaves),
                    ),
                )
            else:
                grouping = [[(c[0], [self.fld_map[f] for f in c[1]]) for c in x] for x in self.grouping]

            return render_template("test/form/form.html", mains=mains, grouping=grouping)
        except Exception as exc:
            error(unicode(exc))
            raise