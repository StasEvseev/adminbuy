#coding: utf-8\n__author__ = 'StasEvseev'
from flask.ext.admin.contrib.sqla import ModelView
from wtforms import TextField, StringField, BooleanField, DecimalField, IntegerField, DateField

from angular.field import TextFieldBootstrap, BooleanBootstrap, DecimalFieldBootstrap, DateFieldBootstrap, \
    CheckBox
from angular.field.form import FormBootstrap
from old.angular.fieldview import FieldWidget
from helper import get_relation_model
from log import error, warning
from db import db


class Form(object):
    """
    Объект, конвертирующий форму flask в форму bootstrap.
    """
    def __init__(self, model):
        self.view = ModelView(model, db.session)

    def scaf_relation_fields(self, form_columns):
        """
        Собираем поля связанных моделей, с именем аттрибута содержащий '.'.
        """
        rel_models = [
            (get_relation_model(self.view.model, x.split(".")[0]), x, dict(form_label=form_columns[x][0]))
            for x in form_columns.keys() if "." in x]
        ext_filds = []
        for m, at, d in rel_models:
            v = ModelView(m, db.session)
            at_f = at.split(".")[1]
            v.form_columns = [at_f]
            f_ = v.scaffold_form()
            ext_filds.append((at, getattr(f_, at_f)))
        return ext_filds

    def scaf_non_model(self, form_columns):
        return [key for (key, value) in form_columns.iteritems() if getattr(value, 'non_model', False)]

    def scaf_fields(self, form_columns):
        return [key for (key, value) in form_columns.iteritems() if not (getattr(value, 'non_model', False) or "." in key)]

    def filter_fields(self, columns):
        return [x for x in columns if x not in ['none']], [x for x in columns if x in ['none']]

    def create_form(self, form_columns, main_attrs, grouping):
        try:
            form_bootstrap = FormBootstrap()
            form_bootstrap.set_group(grouping)

            self.view.form_columns = self.scaf_fields(form_columns)
            nnm = self.scaf_non_model(form_columns)
            self.view.form_columns, non_models = self.filter_fields(self.view.form_columns)
            ext_filds = self.scaf_relation_fields(form_columns)

            form_scaffold = self.view.scaffold_form()

            for at, ext_f in ext_filds:
                setattr(form_scaffold, at, ext_f)

            for nmf in non_models:
                setattr(form_scaffold, nmf, form_columns[nmf])

            for nmf in nnm:
                setattr(form_scaffold, nmf, form_columns[nmf])

            for col in form_columns.keys():
                is_main = False
                field_cls = getattr(form_scaffold, col, None)
                if field_cls is None:
                    if col in form_columns:
                        field = form_columns[col]
                    else:
                        warning(u"Не создается поле %s на форму." % col)
                        continue
                else:
                    field = form_columns[col]

                if main_attrs and col in main_attrs:
                    is_main = True
                if isinstance(field, FieldWidget):
                    form_bootstrap.add_field(field.field(is_main))
                elif isinstance(field, (TextFieldBootstrap, DecimalFieldBootstrap, CheckBox, DateFieldBootstrap,
                        BooleanBootstrap)):
                    field.is_main = is_main
                    form_bootstrap.add_field(field)
                else:
                    label, place = field
                    if field_cls.field_class in (TextField, StringField):
                        form_bootstrap.add_field(TextFieldBootstrap(
                            id=col, label=label, placeholder=place, is_main=is_main))
                    elif field_cls.field_class in (BooleanField, ):
                        form_bootstrap.add_field(BooleanBootstrap(id=col, label=label))
                    elif field_cls.field_class in (DecimalField, IntegerField):
                        form_bootstrap.add_field(DecimalFieldBootstrap(
                            id=col, label=label, placeholder=place, is_main=is_main))
                    elif field_cls.field_class in (DateField, ):
                        form_bootstrap.add_field(DateFieldBootstrap(id=col, label=label))
                    else:
                        warning(u"Новый необрабатываемый тип поля %s." % field_cls.field_class)
            return form_bootstrap
        except Exception as exc:
            error(unicode(exc))
            raise