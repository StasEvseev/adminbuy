#coding: utf-8

__author__ = 'StasEvseev'


# class TestProviderUi(UiTest):
#
#     id_item = 'providerangularview'
#
#     def form_field(self):
#         name_fld = get_input(self.driver, "name")
#         address_fld = get_input(self.driver, "address")
#         emails_fld = get_input(self.driver, "emails")
#         return name_fld, address_fld, emails_fld
#
#     def view_field(self):
#         name_fld = get_main_input(self.driver, "name")
#         address_fld = get_view_input(self.driver, "address")
#         emails_fld = get_view_input(self.driver, "emails")
#         return name_fld, address_fld, emails_fld
#
#     def test_server_is_up_and_running(self):
#         self.login()
#         name = u"Имя"
#         address = u"Адрес"
#         emails = "name@name.ru"
#         name_2 = u"Имя не сохраненное"
#         address_2 = u"Адрес не сохраненный"
#         emails_2 = u"email@notsave.ru"
#         name_3 = u"Саша"
#         address_3 = u"Адресочек непонятный"
#         emails_3 = "name2@name.ru"
#         name_4 = u"Петя"
#         address_4 = u"Адресочек кажется Петин"
#         emails_4 = "name3@name.ru"
#
#         self.open()
#
#         self.create()
#         name_fld, address_fld, emails_fld = self.form_field()
#         name_fld.send_keys(name)
#         address_fld.send_keys(address)
#         emails_fld.send_keys(emails)
#
#         self.save()
#         name_fld, address_fld, emails_fld = self.view_field()
#         self.assertEqual(name_fld.text, name)
#         self.assertEqual(address_fld.text, address)
#         self.assertEqual(emails_fld.text, emails)
#
#         self.edit()
#         name_fld, address_fld, emails_fld = self.form_field()
#         name_fld.clear()
#         name_fld.send_keys(name_2)
#         address_fld.clear()
#         address_fld.send_keys(address_2)
#         emails_fld.clear()
#         emails_fld.send_keys(emails_2)
#         self.cancel()
#         name_fld, address_fld, emails_fld = self.view_field()
#         self.assertEqual(name_fld.text, name)
#         self.assertEqual(address_fld.text, address)
#         self.assertEqual(emails_fld.text, emails)
#
#         self.edit()
#         name_fld, address_fld, emails_fld = self.form_field()
#         name_fld.clear()
#         name_fld.send_keys(name_3)
#         address_fld.clear()
#         address_fld.send_keys(address_3)
#         emails_fld.clear()
#         emails_fld.send_keys(emails_3)
#
#         self.save()
#         name_fld, address_fld, emails_fld = self.view_field()
#         self.assertEqual(name_fld.text, name_3)
#         self.assertEqual(address_fld.text, address_3)
#         self.assertEqual(emails_fld.text, emails_3)
#
#         self.root()
#         rows = self.table_rows()
#         self.assertEqual(len(rows), 1)
#         empty_rows = self.table_rows_empty()
#         self.assertEqual(len(empty_rows), 3)
#
#         self.rows_click(rows, 0)
#
#         self.create()
#         name_fld, address_fld, emails_fld = self.form_field()
#         name_fld.send_keys(name_4)
#         address_fld.send_keys(address_4)
#         emails_fld.send_keys(emails_4)
#
#         self.save()
#         name_fld, address_fld, emails_fld = self.view_field()
#         self.assertEqual(name_fld.text, name_4)
#         self.assertEqual(address_fld.text, address_4)
#         self.assertEqual(emails_fld.text, emails_4)
#
#         self.root()
#         rows = self.table_rows()
#         self.assertEqual(len(rows), 2)
#         empty_rows = self.table_rows_empty()
#         self.assertEqual(len(empty_rows), 2)
#
#         self.rows_click(rows, 0)
#         self.delete()
#         btn_ok, btn_cancel = get_confirm_btns(self.driver)
#         btn_cancel.click()
#         WebDriverWait(self.driver, 2).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "div.form-sheet")))
#
#         self.root()
#         rows = self.table_rows()
#         self.assertEqual(len(rows), 2)
#         empty_rows = self.table_rows_empty()
#         self.assertEqual(len(empty_rows), 2)
#
#         self.rows_click(rows, 0)
#         self.delete()
#         btn_ok, btn_cancel = get_confirm_btns(self.driver)
#         btn_ok.click()
#
#         rows = self.table_rows()
#         self.assertEqual(len(rows), 1)
#         empty_rows = self.table_rows_empty()
#         self.assertEqual(len(empty_rows), 3)
