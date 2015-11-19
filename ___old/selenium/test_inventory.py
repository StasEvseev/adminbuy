#coding: utf-8\n__author__ = 'StasEvseev'
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from applications.good.model import Good
from all.helpers.suits.application import ApplicationSuite
from all.selenium.test_common_ui import (
    CommonTestUi, fill_input, data_form, fill_form, check_data, select_item_dict_select, get_tabpanel,
    add_to_local_table, click_btn_modal, rows_local_table, add_btn_local_table, get_button_from_extra)
from applications.inventory.views import InventoryView
from all.selenium.test_ui import get_modal_btns, get_confirm_btns


def _td_rows_local_table(row):
    ths_1 = row.find_elements_by_css_selector("td.good_full_name")[0]
    ths_2 = row.find_elements_by_css_selector("td.count_before")[0]
    ths_3 = row.find_elements_by_css_selector("td.count_after")[0]
    return ths_1, ths_2, ths_3


class InventoryUi(CommonTestUi):
    VIEW = InventoryView

    def create_app(self):
        app = super(InventoryUi, self).create_app()
        self.client = app.test_client()
        self.app_suite = ApplicationSuite(self.client, app)

        self.GOOD = (u"номенклатура", '1', '15', 4.0, 3.0)
        self.GOOD2 = (u"номенклатура2", '115', '634', 5.7, 4.5)
        self.GOOD3 = (u"номенклатура3", '67', '943', 22.0, 19.5)
        self.GOOD4 = (u"номенклатура4", '123', '345', 53.5, 45.0)
        self.GOOD5 = (u"Номенклатура5", None, None, 200.0, 170.0)

        self.GOODS = (self.GOOD, self.GOOD2, self.GOOD3, self.GOOD4, self.GOOD5)

        self.MAP_GOOD = {}

        self.field_id_good = "good"
        self.field_id_count_before = "count_before"
        self.field_id_count_after = "count_after"

        self.index_1 = 0
        self.index_2 = 1
        self.index_3 = 2
        self.index_4 = 3
        self.index_5 = 4

        self.count_before = ""

        self.count_after_1 = "1"
        self.count_after_2 = "2"
        self.count_after_3 = "3"
        self.count_after_4 = "4"
        self.count_after_5 = "5"

        self.instance = self.VIEW()
        self.form = self.instance.get_form()
        self.form_columns = self.instance.form_columns
        self.main_attrs = self.instance.main_attrs

        with app.app_context():
            for good_d in self.GOODS:
                name, nl, ng, pr_r, pr_g = good_d
                good_id = self.app_suite.good(name, nl, ng, pr_r, pr_g)
                good = Good.query.get(good_id)
                self.MAP_GOOD[good_id - 1] = good.full_name
        return app

    def testStatuses(self):
        self.login()
        self.open_item(self.instance.get_id())
        #Ну а теперь проверим по медленному.
        # self.root()
        self.create()
        data2 = data_form(self.form, self.form_columns)
        fill_form(self.driver, data2, self.main_attrs)
        self.save()
        check_data(self, self.driver, data2, self.main_attrs)

        tabs = get_tabpanel(self.driver)
        self.assertEqual(tabs.is_displayed(), False)

        btn_first = get_button_from_extra(self.driver, 0)
        btn_second = get_button_from_extra(self.driver, 1)
        btn_third = get_button_from_extra(self.driver, 2)
        self.assertEqual(btn_first.is_displayed(), True)
        self.assertEqual(btn_second.is_displayed(), False)
        self.assertEqual(btn_third.is_displayed(), False)

        btn_first.click()

        # WebDriverWait(self.driver, 30).until(expected_conditions.invisibility_of_element_located(
        #     (By.CSS_SELECTOR, "#page-wrapper > div > div > header > button.btn-extra-1")
        # ))
        #
        # WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
        #     (By.CSS_SELECTOR, "#page-wrapper > div > div > header > button.btn-extra-2")
        # ))
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.form-sheet")))
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, "button.btn-extra-2")))
        tabs = get_tabpanel(self.driver)
        self.assertEqual(tabs.is_displayed(), True)
        btn_first = get_button_from_extra(self.driver, 0)
        btn_second = get_button_from_extra(self.driver, 1)
        btn_third = get_button_from_extra(self.driver, 2)
        self.assertEqual(btn_first.is_displayed(), False)
        self.assertEqual(btn_second.is_displayed(), True)
        self.assertEqual(btn_third.is_displayed(), True)

        add_btn = add_btn_local_table(self.driver)
        self.assertEqual(add_btn.is_displayed(), False)

        self.edit()

        add_btn = add_btn_local_table(self.driver)
        self.assertEqual(add_btn.is_displayed(), True)

        add_to_local_table(self.driver)
        select_item_dict_select(self.driver, self.field_id_good, self.index_1)
        fill_input(self.driver, self.field_id_count_before, self.count_before)
        fill_input(self.driver, self.field_id_count_after, self.count_after_1)
        (btn_ok, _), _ = get_modal_btns(self.driver)
        click_btn_modal(btn_ok, self.driver)

        add_to_local_table(self.driver)
        select_item_dict_select(self.driver, self.field_id_good, self.index_2)
        fill_input(self.driver, self.field_id_count_before, self.count_before)
        fill_input(self.driver, self.field_id_count_after, self.count_after_2)
        (btn_ok, _), _ = get_modal_btns(self.driver)
        click_btn_modal(btn_ok, self.driver)

        self.save()
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.form-sheet")))
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.form-sheet")))
        rows = rows_local_table(self.driver)
        self.assertEqual(len(rows), 2)
        for row in rows:
            btn_rem = row.find_elements_by_css_selector("td.td-remove > span > div.btn-remove")[0]
            self.assertEqual(btn_rem.is_displayed(), False)

        btn_first = get_button_from_extra(self.driver, 0)
        btn_second = get_button_from_extra(self.driver, 1)
        btn_third = get_button_from_extra(self.driver, 2)
        self.assertEqual(btn_first.is_displayed(), False)
        self.assertEqual(btn_second.is_displayed(), True)
        self.assertEqual(btn_third.is_displayed(), True)

        # btn_third.click()
        # WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
        #     (By.CSS_SELECTOR, "div.form-sheet")))
        # WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
        #     (By.CSS_SELECTOR, "button.btn-extra-1")))
        #
        # tabs = get_tabpanel(self.driver)
        # self.assertEqual(tabs.is_displayed(), False)
        #
        # btn_first = get_button_from_extra(self.driver, 0)
        # btn_second = get_button_from_extra(self.driver, 1)
        # btn_third = get_button_from_extra(self.driver, 2)
        # self.assertEqual(btn_first.is_displayed(), True)
        # self.assertEqual(btn_second.is_displayed(), False)
        # self.assertEqual(btn_third.is_displayed(), False)
        #
        # btn_first.click()
        # WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
        #     (By.CSS_SELECTOR, "div.form-sheet")))
        # WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
        #     (By.CSS_SELECTOR, "button.btn-extra-2")))
        #
        # tabs = get_tabpanel(self.driver)
        # self.assertEqual(tabs.is_displayed(), True)
        #
        # rows = rows_local_table(self.driver)
        # self.assertEqual(len(rows), 2)
        #
        # btn_first = get_button_from_extra(self.driver, 0)
        # btn_second = get_button_from_extra(self.driver, 1)
        # btn_third = get_button_from_extra(self.driver, 2)
        # self.assertEqual(btn_first.is_displayed(), False)
        # self.assertEqual(btn_second.is_displayed(), True)
        # self.assertEqual(btn_third.is_displayed(), True)
        #
        # btn_second.click()
        # WebDriverWait(self.driver, 30).until(expected_conditions.invisibility_of_element_located(
        #     (By.CSS_SELECTOR, "button.btn-extra-2")))
        #
        # tabs = get_tabpanel(self.driver)
        # self.assertEqual(tabs.is_displayed(), True)
        #
        # rows = rows_local_table(self.driver)
        # self.assertEqual(len(rows), 2)
        #
        # btn_first = get_button_from_extra(self.driver, 0)
        # btn_second = get_button_from_extra(self.driver, 1)
        # btn_third = get_button_from_extra(self.driver, 2)
        # self.assertEqual(btn_first.is_displayed(), False)
        # self.assertEqual(btn_second.is_displayed(), False)
        # self.assertEqual(btn_third.is_displayed(), False)
        #
        # self.edit()
        #
        # add_btn = add_btn_local_table(self.driver)
        # self.assertEqual(add_btn.is_displayed(), False)

    def testTabsCRUD(self):

        self.login()
        self.open_item(self.instance.get_id())

        self.create()
        tabs = get_tabpanel(self.driver)
        self.assertEqual(tabs.is_displayed(), False)
        data = data_form(self.form, self.form_columns)
        fill_form(self.driver, data, self.main_attrs)

        btn_first = get_button_from_extra(self.driver, 0)
        btn_second = get_button_from_extra(self.driver, 1)
        btn_third = get_button_from_extra(self.driver, 2)
        self.assertEqual(btn_first.is_displayed(), True)
        self.assertEqual(btn_second.is_displayed(), False)
        self.assertEqual(btn_third.is_displayed(), False)

        btn_first.click()
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.form-sheet")))

        tabs = get_tabpanel(self.driver)
        self.assertEqual(tabs.is_displayed(), True)

        add_btn = add_btn_local_table(self.driver)
        self.assertEqual(add_btn.is_displayed(), False)
        self.edit()

        btn_first = get_button_from_extra(self.driver, 0)
        btn_second = get_button_from_extra(self.driver, 1)
        btn_third = get_button_from_extra(self.driver, 2)
        self.assertEqual(btn_first.is_displayed(), False)
        self.assertEqual(btn_second.is_displayed(), True)
        self.assertEqual(btn_third.is_displayed(), True)

        self.save()
        check_data(self, self.driver, data, self.main_attrs)

        tabs = get_tabpanel(self.driver)
        self.assertEqual(tabs.is_displayed(), True)

        add_btn = add_btn_local_table(self.driver)
        self.assertEqual(add_btn.is_displayed(), False)

        btn_first = get_button_from_extra(self.driver, 0)
        btn_second = get_button_from_extra(self.driver, 1)
        btn_third = get_button_from_extra(self.driver, 2)
        self.assertEqual(btn_first.is_displayed(), False)
        self.assertEqual(btn_second.is_displayed(), True)
        self.assertEqual(btn_third.is_displayed(), True)

        self.edit()
        add_btn = add_btn_local_table(self.driver)
        self.assertEqual(add_btn.is_displayed(), True)
        add_to_local_table(self.driver)
        select_item_dict_select(self.driver, self.field_id_good, self.index_1)
        fill_input(self.driver, self.field_id_count_before, self.count_before)
        fill_input(self.driver, self.field_id_count_after, self.count_after_1)

        (btn_ok, _), _ = get_modal_btns(self.driver)
        click_btn_modal(btn_ok, self.driver)

        rows = rows_local_table(self.driver)
        self.assertEqual(len(rows), 1)

        row = rows[0]
        ths_1, ths_2, ths_3 = _td_rows_local_table(row)
        self.assertEqual(ths_1.text, self.MAP_GOOD[self.index_5])
        self.assertEqual(ths_2.text, self.count_before)
        self.assertEqual(ths_3.text, self.count_after_1)

        add_to_local_table(self.driver)
        select_item_dict_select(self.driver,  self.field_id_good,  self.index_2)
        fill_input(self.driver,  self.field_id_count_before,  self.count_before)
        fill_input(self.driver,  self.field_id_count_after,  self.count_after_2)

        _, btn_cancel = get_modal_btns(self.driver)
        click_btn_modal(btn_cancel, self.driver)

        rows = rows_local_table(self.driver)
        self.assertEqual(len(rows), 1)

        add_to_local_table(self.driver)
        select_item_dict_select(self.driver,  self.field_id_good,  self.index_3)
        fill_input(self.driver,  self.field_id_count_before,  self.count_before)
        fill_input(self.driver,  self.field_id_count_after,  self.count_after_3)

        (btn_ok, _), _ = get_modal_btns(self.driver)
        click_btn_modal(btn_ok, self.driver)

        rows = rows_local_table(self.driver)
        self.assertEqual(len(rows), 2)

        row_1 = rows[0]
        row_1.click()
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.modal-dialog")))

        select_item_dict_select(self.driver,  self.field_id_good,  self.index_4)
        fill_input(self.driver,  self.field_id_count_before,  self.count_before)
        fill_input(self.driver,  self.field_id_count_after,  self.count_after_4)
        _, btn_cancel = get_modal_btns(self.driver)
        click_btn_modal(btn_cancel, self.driver)

        rows = rows_local_table(self.driver)
        self.assertEqual(len(rows), 2)
        row_1 = rows[0]
        ths_1, ths_2, ths_3 = _td_rows_local_table(row_1)
        self.assertEqual(ths_1.text, self.MAP_GOOD[self.index_5])
        self.assertEqual(ths_2.text,  self.count_before)
        self.assertEqual(ths_3.text,  self.count_after_1)

        row_2 = rows[1]
        row_2.click()
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.modal-dialog")))

        select_item_dict_select(self.driver,  self.field_id_good,  self.index_5)
        fill_input(self.driver,  self.field_id_count_before,  self.count_before)
        fill_input(self.driver,  self.field_id_count_after,  self.count_after_5)
        (_, btn_ok_edit), _ = get_modal_btns(self.driver)
        click_btn_modal(btn_ok_edit, self.driver)

        rows = rows_local_table(self.driver)
        self.assertEqual(len(rows), 2)
        row_2 = rows[1]
        ths_1, ths_2, ths_3 = _td_rows_local_table(row_2)
        self.assertEqual(ths_1.text, self.MAP_GOOD[self.index_1])
        self.assertEqual(ths_2.text,  self.count_before)
        self.assertEqual(ths_3.text,  self.count_after_5)

        row_1 = rows[0]
        btn_rem = row_1.find_elements_by_css_selector("td.td-remove > span > div.btn-remove")[0]
        btn_rem.click()

        rows = rows_local_table(self.driver)
        self.assertEqual(len(rows), 1)

        btn_first = get_button_from_extra(self.driver, 0)
        btn_second = get_button_from_extra(self.driver, 1)
        btn_third = get_button_from_extra(self.driver, 2)
        self.assertEqual(btn_first.is_displayed(), False)
        self.assertEqual(btn_second.is_displayed(), True)
        self.assertEqual(btn_third.is_displayed(), True)

        btn_second.click()
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.form-sheet")))

        tabs = get_tabpanel(self.driver)
        self.assertEqual(tabs.is_displayed(), True)

        btn_ok, btn_c = get_confirm_btns(self.driver)
        btn_ok.click()
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, "div.form-sheet")))
        add_btn = add_btn_local_table(self.driver)
        self.assertEqual(add_btn.is_displayed(), False)

        btn_first = get_button_from_extra(self.driver, 0)
        btn_second = get_button_from_extra(self.driver, 1)
        btn_third = get_button_from_extra(self.driver, 2)
        self.assertEqual(btn_first.is_displayed(), False)
        self.assertEqual(btn_second.is_displayed(), False)
        self.assertEqual(btn_third.is_displayed(), False)