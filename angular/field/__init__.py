#coding: utf-8
from flask import render_template
from log import error

from angular.field.behavior import BehaviorHiddenPredicate
from angular.field.validator import RequiredValidator


class FieldBootstrap(object):
    def __init__(self, **kwargs):
        self.scope = "$scope"
        self.label = None
        self.id = None
        self.prefix = "model"
        self.is_main = False
        self.required = False
        self.behaviors = None
        self.validators = None
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        if "." in self.id:
            self.id_form = self.id.replace(".", "_")
            self.id_s = "['" + self.id + "']"
        else:
            self.id_form = self.id
            self.id_s = "." + self.id
        self.behaviors = self.behaviors or []
        self.validators = self.validators or []

        if self.required:
            self.validators.append(RequiredValidator(
                message=u"Заполните поле '%s'" % self.label))

        for val in self.validators:
            val.initial(id=self.id, label=self.label, prefix=".".join([self.scope, self.prefix]))

    def initialize_controller(self):
        return ""

    def render(self):
        pass

    def get_form_id(self):
        return self.id

    def get_form_attr(self):
        return self.scope + "." + self.prefix + self.id_s


class BooleanBootstrap(FieldBootstrap):
    def __init__(self, **kwargs):
        self.is_check = False
        self.is_main = False
        super(BooleanBootstrap, self).__init__(**kwargs)

    def render(self, **kwargs):
        kwargs['label'] = self.label
        kwargs['id'] = self.id
        kwargs['id_form'] = self.id_form
        kwargs['id_s'] = self.id_s
        kwargs['prefix'] = self.prefix
        # kwargs['is_check'] = {True: 'true', False: 'false'}[self.is_check]
        try:
            return render_template("test/form/checkbox_field.html", **kwargs)
        except Exception as exc:
            error(unicode(exc))
            raise

    def initialize_controller(self):
        if self.is_check:
            return self.scope + "." + self.prefix + self.id_s + " = %s;" % 'true'
        else:
            return ""


class DictSelectField(FieldBootstrap):

    def __init__(self, **kwargs):
        self.tostring = ""
        self.modal_cntr = ""
        self.modal_id = ""
        self.placeholder = ""
        self.link = None
        self.can_create = False
        self.can_edit = False
        super(DictSelectField, self).__init__(**kwargs)
        self.id_s = self.id + '_id'

    def render(self, **kwargs):
        kwargs['label'] = self.label
        kwargs['id'] = self.id
        kwargs['id_form'] = self.id_form
        kwargs['prefix'] = self.prefix
        kwargs['modal_cntr'] = self.modal_cntr
        kwargs['modal_id'] = self.modal_id
        kwargs['tostring'] = self.tostring
        kwargs['placeholder'] = self.placeholder
        kwargs['is_main'] = 'true' if self.is_main else 'false'
        beh_v = [x for x in self.behaviors if isinstance(x, BehaviorHiddenPredicate)]
        kwargs['behavior_view'] = beh_v[0] if beh_v else None
        kwargs['link'] = self.link or ""
        kwargs['can_create'] = 'true' if self.can_create else 'false'
        kwargs['can_edit'] = 'true' if self.can_edit else 'false'
        try:
            return render_template("test/form/dict_select_field.html", **kwargs)
        except Exception as exc:
            error(unicode(exc))
            raise

    def get_form_id(self):
        return self.id_s

    def get_form_attr(self):
        return self.scope + "." + self.prefix + "." + self.id + " ? " + self.scope + "." + self.prefix + "." + self.id + ".id" + " : -1" # + self.scope + "." + self.prefix + "." + self.id


class CheckBox(FieldBootstrap):
    def __init__(self, **kwargs):
        self.items = []
        self.default_value = None
        super(CheckBox, self).__init__(**kwargs)

    def render(self, **kwargs):
        kwargs['items'] = self.items
        kwargs['label'] = self.label
        kwargs['id'] = self.id
        kwargs['id_s'] = self.id_s
        kwargs['prefix'] = self.prefix
        kwargs['default_value'] = self.default_value
        try:
            return render_template("test/form/radiobox_field.html", **kwargs)
        except Exception as exc:
            error(unicode(exc))
            raise

    def initialize_controller(self):
        if self.default_value:
            return self.scope + "." + self.prefix + self.id_s + " = %s;" % self.default_value
        else:
            return ""


class DecimalFieldBootstrap(FieldBootstrap):
    def __init__(self, **kwargs):
        self.placeholder = ''
        self.is_main = False
        self.main = False
        self.input_group = False
        self.input_group_exp = ""
        self.input_group_popup = ""
        super(DecimalFieldBootstrap, self).__init__(**kwargs)

    def render(self, **kwargs):
        kwargs['label'] = self.label
        kwargs['id'] = self.id
        kwargs['id_s'] = self.id_s
        kwargs['id_form'] = self.id_form
        kwargs['prefix'] = self.prefix
        kwargs['placeholder'] = self.placeholder
        kwargs['is_main'] = self.is_main
        kwargs['main'] = self.main
        kwargs['input_group'] = self.input_group
        kwargs['input_group_exp'] = self.input_group_exp
        kwargs['input_group_popup'] = self.input_group_popup
        try:
            return render_template("test/form/decimal_field.html", **kwargs)
        except Exception as exc:
            error(unicode(exc))
            raise


class DateFieldBootstrap(FieldBootstrap):
    def render(self, **kwargs):
        kwargs['label'] = self.label
        kwargs['id_form'] = self.id_form
        kwargs['prefix'] = self.prefix
        try:
            return render_template("test/form/datefield.html", **kwargs)
        except Exception as exc:
            error(unicode(exc))
            raise

    def get_form_attr(self):
        return self.scope + "." + self.prefix + "." + self.id_form


class TextFieldBootstrap(FieldBootstrap):
    def __init__(self, **kwargs):
        self.placeholder = ""
        self.is_main = False
        self.main = False
        self.filter = None
        super(TextFieldBootstrap, self).__init__(**kwargs)

    def render(self, **kwargs):
        kwargs['label'] = self.label
        kwargs['id'] = self.id
        kwargs['id_s'] = self.id_s
        kwargs['id_form'] = self.id_form
        kwargs['prefix'] = self.prefix
        kwargs['placeholder'] = self.placeholder
        kwargs['is_main'] = self.is_main
        kwargs['main'] = self.main
        beh_v = [x for x in self.behaviors if isinstance(x, BehaviorHiddenPredicate)]
        kwargs['behavior_view'] = beh_v[0] if beh_v else None
        kwargs['filter'] = self.filter
        try:
            return render_template("test/form/text_field.html", **kwargs)
        except Exception as exc:
            error(unicode(exc))
            raise