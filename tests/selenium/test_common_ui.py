#coding: utf-8\n__author__ = 'StasEvseev'
from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from old.angular.field import TextFieldBootstrap, DictSelectField, DecimalFieldBootstrap, BehaviorHiddenPredicate
from tests.helpers import Generator
from tests.selenium.test_ui import (
    UiTest, get_input, get_view_input, get_main_input, get_confirm_btns, get_dict_select_field, get_modal_btns,
    get_view_dict_select_field, get_mainview_dict_select_field)
from old.admin import InventoryView, ProviderAngularView, PointSaleAngularView, CommodityAngularView


def data_form(form, form_columns):
    res = {}
    for col in form_columns.keys():
        try:
            fld = form.fld_map[col]
        except KeyError:
            continue
        if fld.behaviors and BehaviorHiddenPredicate in [x.__class__ for x in fld.behaviors]:
            continue

        res[col] = (fld, _gen_data(fld))
    return res


def _gen_data(fld):
    if isinstance(fld, TextFieldBootstrap):
        return Generator.generate_string(20)
    elif isinstance(fld, DictSelectField):
        return Generator.generate_string(30)
    elif isinstance(fld, DecimalFieldBootstrap):
        return Generator.generate_int(max=10)


def select_item_dict_select(driver, el_id, index, main=False):
    inpt = get_dict_select_field(driver, el_id, main)
    dictSelectField = FieldTestDictSelect(inpt, el_id, driver, main)
    dictSelectField.click_btn_search(li=True)
    dictSelectField.click_item(index)


class FieldTestDictSelect(object):

    def __init__(self, elem, id, driver, main=False):
        self.elem = elem
        self.id = id
        self.driver = driver
        self.is_main = main

    def _major_csspath(self):
        if self.is_main:
            return "div.mainview-dict-select-field-%s" % self.id
        else:
            return "div.dict-select-field-%s" % self.id

    def _path_to_extra_buttons(self):
        return "div > div:nth-child(2) > div:nth-child(2)"

    def clear(self):
        btn_clear = self.elem.find_elements(
            By.CSS_SELECTOR, self._path_to_extra_buttons() + " > i.dsf-btn-clr")[0]
        if btn_clear.is_displayed():
            btn_clear.click()
            WebDriverWait(self.driver, 30).until(expected_conditions.invisibility_of_element_located(
                (By.CSS_SELECTOR, self._major_csspath() + " > " + self._path_to_extra_buttons() + " > i.dsf-btn-clr")))

    def btn_search(self):
        return self.elem.find_elements(
            By.CSS_SELECTOR, "div > div:nth-child(2) > div:nth-child(2) > div > div > button.ui-select-match")[0]

    def btn_create(self):
        return self.elem.find_elements(
            By.CSS_SELECTOR, "div > div:nth-child(2) > div:nth-child(2) > span > i.dsf-btn-crt")[0]

    def li(self):
        return self.elem.find_elements(
            By.CSS_SELECTOR, "div > div:nth-child(2) > div:nth-child(2) > div > div > ul > li")[0]

    def items(self):
        return self.li().find_elements(By.CSS_SELECTOR, "div.ui-select-choices-row")

    def click_btn_search(self, li=False):
        self.btn_search().click()
        if li:
            if self.is_main:
                WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
                    (By.CSS_SELECTOR,
                     "div.mainview-dict-select-field-%s > div > div:nth-child(2) > div:nth-child(2) > div > div > ul" % self.id)))
            else:
                WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
                    (By.CSS_SELECTOR,
                     "div.dict-select-field-%s > div > div:nth-child(2) > div:nth-child(2) > div > div > ul" % self.id)))
        else:
            if self.is_main:
                WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
                    (By.CSS_SELECTOR,
                     "div.mainview-dict-select-field-%s > div > div:nth-child(2) > div:nth-child(2) > div > div > input.ui-select-search" % self.id)))
            else:
                WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
                    (By.CSS_SELECTOR,
                     "div.dict-select-field-%s > div > div > div:nth-child(2) > div > div > input.ui-select-search" % self.id)))

    def click_item(self, index):
        items = self.items()
        list(items)[index].click()

        WebDriverWait(self.driver, 30).until(expected_conditions.invisibility_of_element_located(
            (By.CSS_SELECTOR,
             self._major_csspath() + " > div > span > span > div:nth-child(2) > div > div > ul")))


def _fill_dict_select(driver, el_id, data, fld, main=False):

    def crt():
        crt_bnt.click()
        WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, 'div.modal-dialog')))
        inner_input = get_input(driver, fld.tostring)
        inner_input.send_keys(data)
        (btn_ok, _), btn_cl = get_modal_btns(driver)
        btn_ok.click()
        WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.form-sheet")))

    inpt = get_dict_select_field(driver, el_id, main)

    dictselectfield = FieldTestDictSelect(inpt, el_id, driver, main)
    dictselectfield.clear()

    if data:

        crt_bnt = dictselectfield.btn_create()
        dictselectfield.click_btn_search()

        li_el = inpt.find_elements(By.CSS_SELECTOR, "li.ui-select-choices-group")[0]
        if li_el.is_displayed():
            input_fld = inpt.find_elements(By.CSS_SELECTOR, "input.ui-select-search")[0]
            input_fld.send_keys(data)
            # WebDriverWait(driver, 30).until(expected_conditions.invisibility_of_element_located(
            #     (By.CSS_SELECTOR, "li.ui-select-choices-group")))
            # WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located(
            #     (By.CSS_SELECTOR, "span.spinner")))
            WebDriverWait(driver, 30).until(expected_conditions.invisibility_of_element_located(
                (By.CSS_SELECTOR, "span.spinner-%s%s" % (el_id, "-main" if main else ""))))
            # WebDriverWait(driver, 30).until(expected_conditions.invisibility_of_element_located(
            #     (By.CSS_SELECTOR, "span.spinner-%s%s" % (el_id, "-main" if main else ""))))
            li_el = driver.find_elements(By.CSS_SELECTOR, "li.ui-select-choices-group")[0]
            if li_el.is_displayed():
                dictselectfield.click_item(0)
            else:
                crt()
        else:
            crt()


def fill_input(driver, el_id, data):
    inpt = get_input(driver, el_id)
    inpt.clear()
    if data is not None:
        inpt.send_keys(data)
    else:
        inpt.send_keys()


def fill_form(driver, data, main_attrs):
    for item in data.keys():
        fld, d = data[item]
        id_form = item.replace(".", "_") if "." in item else item
        if isinstance(fld, (TextFieldBootstrap, DecimalFieldBootstrap)):
            fill_input(driver, id_form, d)
        elif isinstance(fld, DictSelectField):
            _fill_dict_select(driver, id_form, d, fld, main=item in main_attrs)


def check_data(testcase, driver, data, main_attrs):
    for item in data.keys():
        fld, d = data[item]
        if isinstance(fld, TextFieldBootstrap):
            if item in main_attrs:
                elm = get_main_input(driver, item)
            else:
                elm = get_view_input(driver, item)
            testcase.assertEqual(elm.text, d, u"В поле %s лежит неправильное значение. %s != %s" % (item, elm.text, d))
        elif isinstance(fld, DictSelectField):
            if item in main_attrs:
                elm = get_mainview_dict_select_field(driver, item)
            else:
                elm = get_view_dict_select_field(driver, item)
            testcase.assertEqual(elm.text, d)


def _check_in_db(testcase, model_instance, data):
    for item in data.keys():
        fld, d = data[item]
        if isinstance(fld, DictSelectField):
            nest = getattr(model_instance, item)
            testcase.assertEqual(getattr(nest, fld.tostring), d)
        else:
            if isinstance(fld, (TextFieldBootstrap, DecimalFieldBootstrap)):
                if "." in item:
                    nest_m = model_instance
                    for it in item.split("."):
                        nest_m = getattr(nest_m, it)
                    if nest_m:
                        if isinstance(nest_m, Decimal):
                            nest_m = int(nest_m)
                        testcase.assertEqual(unicode(nest_m), unicode(d))
                else:
                    testcase.assertEqual(unicode(getattr(model_instance, item)), unicode(d))


def get_tabpanel(driver):
    return driver.find_elements_by_css_selector("div.form-tabs")[0]


def _get_panel_extra(driver):
    return driver.find_elements_by_css_selector("header.panel-extra")[0]


def _get_button_from_panel_extra(panel, index):
    return panel.find_elements_by_tag_name("button")[index]


def get_button_from_extra(driver, index):
    return _get_button_from_panel_extra(_get_panel_extra(driver), index)


def rows_local_table(driver):
    return driver.find_elements_by_css_selector("table.inner-table > tbody > tr.row-local")


def click_btn_modal(btn, driver):
    btn.click()
    WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located(
        (By.CSS_SELECTOR, "div.form-sheet")))


def add_btn_local_table(driver):
    return driver.find_elements_by_css_selector("a.add-item-to-local")[0]


def add_to_local_table(driver):
    add = add_btn_local_table(driver)
    add.click()
    WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located(
        (By.CSS_SELECTOR, "div.modal-dialog")))


class CommonTestUi(UiTest):

    VIEWS = None

    def _test_crud(self):
        self.login()
        if self.VIEWS:
            instance = self.VIEWS()
            with self.app.app_context():
                self._item(instance)

    def _item(self, view):
        url = view.get_id()
        form = view.get_form()
        label_root = view.label_root
        main_attrs = view.main_attrs
        form_columns = view.form_columns

        self.open_item(url)

        nav_first = self.nav_first()
        self.assertEqual(nav_first.text, label_root)

        self.create()
        data = data_form(form, form_columns)
        fill_form(self.driver, data, main_attrs)
        self.save()
        # instance = view.model.query.get(1)
        # check_data(self, self.driver, data, main_attrs)
        # _check_in_db(self, instance, data)

        self.edit()
        current = self.nav_current()

        if view.bread_attr:
            pass
            # value = getattr(instance, view.bread_attr)
            # self.assertEqual(current.text, value)
        else:
            if main_attrs:
                atr = main_attrs[0]
                self.assertEqual(current.text, data[atr][1])
        data2 = data_form(form, form_columns)
        fill_form(self.driver, data2, main_attrs)
        self.cancel()
        # instance_2 = view.model.query.get(1)
        # check_data(self, self.driver, data, main_attrs)
        # _check_in_db(self, instance_2, data)

        self.edit()
        data3 = data_form(form, form_columns)
        fill_form(self.driver, data3, main_attrs)
        self.save()
        # check_data(self, self.driver, data3, main_attrs)

        self.root()
        rows = self.table_rows()
        self.assertEqual(len(rows), 1)
        # self.assertEqual(view.model.query.count(), 1)

        self.rows_click(rows, 0)

        self.create()
        data4 = data_form(form, form_columns)
        fill_form(self.driver, data4, main_attrs)
        self.save()
        # instance_4 = view.model.query.get(2)
        # check_data(self, self.driver, data4, main_attrs)
        # _check_in_db(self, instance_4, data4)

        self.root()
        rows = self.table_rows()
        self.assertEqual(len(rows), 2)
        # self.assertEqual(view.model.query.count(), 2)
        # emrows = self.table_rows_empty()
        # self.assertEqual(len(emrows), 2)

        self.rows_click(rows, 0)
        self.delete()
        btn_ok, btn_cancel = get_confirm_btns(self.driver)
        btn_cancel.click()
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.form-sheet")))

        self.root()
        rows = self.table_rows()
        self.assertEqual(len(rows), 2)
        # self.assertEqual(view.model.query.count(), 2)

        self.rows_click(rows, 0)
        self.delete()
        btn_ok, btn_cancel = get_confirm_btns(self.driver)
        btn_ok.click()

        rows = self.table_rows()
        self.assertEqual(len(rows), 1)
        # self.assertEqual(view.model.query.count(), 1)


class InventoryTest(CommonTestUi):
    VIEWS = InventoryView

    def testInventoryCRUD(self):
        self._test_crud()


class ProviderTest(CommonTestUi):
    VIEWS = ProviderAngularView

    def testProviderCRUD(self):
        self._test_crud()


class PointSaleTest(CommonTestUi):
    VIEWS = PointSaleAngularView

    def testPointSaleCRUD(self):
        self._test_crud()


class CommodityTest(CommonTestUi):
    VIEWS = CommodityAngularView

    def testCommodityCRUD(self):
        self._test_crud()