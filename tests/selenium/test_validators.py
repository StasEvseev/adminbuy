#coding: utf-8
import itertools
import collections
from selenium.common.exceptions import TimeoutException
from angular.field.validator import RequiredValidator, RequiredPredicate
from db import db
from tests.helpers import Generator
from tests.selenium.test_common_ui import _gen_data, fill_form


class Res(object):
    pass


class Any(Res):
    def __init__(self, list):
        self.list = list

    def __repr__(self):
        return "Any - " + str(self.list)


class Concrette(Res):
    def __init__(self, item):
        self.item = item

    def __repr__(self):
        return "Concrette - " + self.item


class ValidatorsMixin(object):
    #TEST VALIDATORS

    def _test_validators(self):
        self.login()
        if self.VIEWS:
            instance = self.VIEWS()
            with self.app.app_context():
                self._item_validators(instance)

    def __prepared_data_to_predicate(self, fields, form_columns, form):
        """
        Формурует данные необходимые для проверки предиката. Работает пока что, только для RequiredPredicate с полем
        DictSelectField.
        """
        #поля с предикатами
        valid = itertools.chain.from_iterable(map(lambda x: filter(lambda y: isinstance(y, RequiredPredicate), x.validators), fields))

        data = {}
        #генерируем имена моделей для условного предиката.
        #для выполнения условия
        commodity_tr = Generator.generate_string(10)
        #для невыполнения условия
        commodity_fl = Generator.generate_string(10)

        for req in valid:
            attr = req.attr_predicate
            data[attr] = (commodity_tr, commodity_fl)

        def get_fld_to_attr_pred(attr):
            if "." in k:
                attr, at = k.split(".")
            return form_columns[attr], form.fld_map[attr]

        for k, d in data.iteritems():
            tr, fl = d
            field, dsf = get_fld_to_attr_pred(k)
            if "." in k:
                _, at = k.split(".")
            view = field.view
            viewmodel = view.model
            inst = viewmodel()
            setattr(inst, dsf.tostring, tr)
            if at:
                setattr(inst, at, True)
            db.session.add(inst)

            inst2 = viewmodel()
            setattr(inst2, dsf.tostring, fl)
            if at:
                setattr(inst2, at, False)
            db.session.add(inst2)

            db.session.commit()

        return data

    #####################################
    def __prepared_data_to_require(self, fields, form_columns, form):
        reqs = itertools.chain.from_iterable(map(lambda x: filter(lambda y: isinstance(y, RequiredValidator), x.validators), fields))

        pass
    #####################################

    def _merge_dicts(self, dcts):

        def get_minimal(values):
            concrs = filter(lambda x: isinstance(x, Concrette), values)
            alls = filter(lambda x: isinstance(x, Any), values)
            nons = filter(lambda x: x is None, values)

            if nons:
                return None

            if concrs and reduce(lambda x, y: x.item == y.item, concrs) is True \
                    and concrs[0].item in set(itertools.chain.from_iterable(map(lambda x: x.list, alls))):
                return concrs[0].item

            if alls:
                res = set(alls[0].list)
                for all in alls:
                    res = res.intersection(all.list)
                if res:
                    return list(res)[0]
            return values[0]

        result = {}
        pre_result = collections.defaultdict(list)

        for dct in dcts:
            for attr, v in dct.iteritems():
                pre_result[attr].append(v)

        for key, res in pre_result.iteritems():
            result[key] = get_minimal(res)
        return result

    def _item_validators(self, view):
        url = view.get_id()
        form = view.get_form()
        label_root = view.label_root
        main_attrs = view.main_attrs
        form_columns = view.form_columns
        model = view.model

        self.open_item(url)
        self.create()

        variance = []
        field_with_validators = filter(lambda x: x.validators, form.fields)
        data = self.__prepared_data_to_predicate(field_with_validators, form_columns, form)
        ALL_OBJ = data.values()
        print "ALL - ", ALL_OBJ[0]
        print "TRUE - ", ALL_OBJ[0][0]
        print "FALSE - ", ALL_OBJ[0][1]

        for fld in field_with_validators:
            validators = fld.validators
            for validator in validators:
                if isinstance(validator, RequiredPredicate):
                    pred = validator.attr_predicate
                    fl, at = pred.split(".")
                    obj_tr = data[pred][0]
                    obj_fl = data[pred][1]
                    variance.append([
                        ({fl: Concrette(obj_fl), fld.id: None}, False),
                        ({fl: Concrette(obj_fl), fld.id: _gen_data(fld)}, False),
                        ({fl: Concrette(obj_tr), fld.id: None}, False),
                        ({fl: Concrette(obj_tr), fld.id: _gen_data(fld)}, True),
                    ])
                elif isinstance(validator, RequiredValidator):
                    variance.append([
                        ({fld.id: None}, False),
                        ({fld.id: Any(ALL_OBJ[0])}, True)
                    ])

        res = list(itertools.product(*variance))

        success = filter(lambda x: all(map(lambda y: y[1], x)), res)
        fails = filter(lambda x: not all(map(lambda y: y[1], x)), res)
        prev_f = None
        prev_dct = None
        for fail in fails:
            dt = {}
            dct = self._merge_dicts(map(lambda x: x[0], fail))
            for k, v in dct.iteritems():
                dt[k] = (form.fld_map[k], v)
            try:
                fill_form(self.driver, dt, main_attrs)
                self.save_js_fail()
            except TimeoutException as exc:
                raise
            except Exception as exc:
                print "CURRENT ", fail
                print "CURRENT ", dct

                print "PREV ", prev_f
                print "PREV ", prev_dct

                pass
                raise
            else:
                prev_f = fail
                prev_dct = dct
            message_cont = self.driver.find_elements_by_id('toast-container')[0]
            self.assertEqual(message_cont.is_displayed(), True)
            # self.cancel()

        for suc in success:
            self.create()
            dt = {}
            dct = self._merge_dicts(map(lambda x: x[0], suc))
            for k, v in dct.iteritems():
                dt[k] = (form.fld_map[k], v)
                fill_form(self.driver, dt, main_attrs)
                self.save()

    ##########################################