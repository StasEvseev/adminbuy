#coding: utf-8
from flask.ext.testing import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import app
from tests import initializetest

LOGIN = "I"
PASS = "I"
EMAIL = 'a@a2.ru'


class VisibleError(Exception):
    pass


def get_modal_btns(driver):
    footer = driver.find_elements(By.CSS_SELECTOR, "div.modal-footer")[0]
    btn_ok = footer.find_elements(By.CSS_SELECTOR, "button.btn-ok")[0]
    btn_ok_edit = footer.find_elements(By.CSS_SELECTOR, "button.btn-ok-edit")[0]
    btn_cl = footer.find_elements(By.CSS_SELECTOR, "a.btn-cl")[0]
    return (btn_ok, btn_ok_edit), btn_cl


def get_confirm_btns(driver):
    footer = driver.find_elements(By.CSS_SELECTOR, "div.modal-footer")[0]
    btns = footer.find_elements(By.CSS_SELECTOR, "button.btn")
    return btns[1], btns[0]


def get_dict_select_field(driver, id, main=False):
    if main:
        return driver.find_elements(By.CSS_SELECTOR, "div.mainview-dict-select-field-%s" % id)[0]
    else:
        return driver.find_elements(By.CSS_SELECTOR, "div.dict-select-field-%s" % id)[0]


def get_view_dict_select_field(driver, id):
    return driver.find_elements(By.CSS_SELECTOR, "span#%s" % id)[0]


def get_mainview_dict_select_field(driver, id):
    return driver.find_elements(By.CSS_SELECTOR, "h3#%s" % id)[0]


def get_input(driver, id):
    return driver.find_elements(By.CSS_SELECTOR, "input#%s" % id)[0]


def get_view_input(driver, id):
    return driver.find_elements(By.CSS_SELECTOR, "span#%s" % id)[0]


def get_main_input(driver, id):
    return driver.find_elements(By.CSS_SELECTOR, "h3#%s" % id)[0]


class UiTest(LiveServerTestCase):
    id_item = ""

    def create_app(self):
        module = app
        application = app.app
        application.config['TESTING'] = True

        initializetest(application)
        application.test_client().post("/admin/register/", data={
            'login': LOGIN,
            'email': EMAIL,
            'password': PASS
        }, follow_redirects=True)

        # # Default port is 5000
        application.config['LIVESERVER_PORT'] = 8943
        self.driver = webdriver.Firefox()

        # def f(engine):
        #     print "ENGINE DISPOSE"
        #     engine.dispose()
        # from multiprocessing.util import register_after_fork
        # with application.app_context():
        #     application.db.engine.dispose()
        #     register_after_fork(application.db.engine, f)
        return application

    def tearDown(self):
        with app.app.app_context():
            app.app.db.engine.dispose()
        self.driver.close()

    def login(self):
        self.driver.get(self.get_server_url())
        self.driver.execute_script("document.getElementsByName('login')[0].value = '%s';" % LOGIN)
        self.driver.execute_script("document.getElementsByName('password')[0].value = '%s';" % PASS)
        self.driver.execute_script("document.getElementsByTagName('form')[0].submit();")

    def open(self):
        self.open_item(self.id_item)

    def open_item(self, id_item):
        menu_item = self.driver.find_element_by_id(id_item)
        menu_item.click()
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, "button.btn-crt")))

    def create(self):
        self.driver.execute_script("$('.btn-crt').click();")
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "div.form-sheet")))

    def edit(self):
        self.driver.execute_script("$('.btn-edt').click();")
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "a.btn-sv")))

    def cancel(self):
        self.driver.execute_script("$('.btn-cl').click();")
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "button.btn-edt")))

    def delete(self):
        drop = self.driver.find_elements(By.CSS_SELECTOR, "button.dropdown-toggle")[0]
        drop.click()
        self.driver.implicitly_wait(30)
        btn = self.driver.find_elements(By.CSS_SELECTOR, "a.btn-del")[0]
        btn.click()
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "div.bootbox-body")))

    def save(self):
        self.driver.execute_script("$('.btn-sv').click();")
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "button.btn-edt")))

    def save_js_fail(self):
        self.driver.execute_script("$('.btn-sv').click();")

    def root(self):
        self.driver.execute_script("$('ol>li:first>a')[0].click();")
        self.driver.implicitly_wait(30)

    def _nav(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "ol.ab-nav")[0]

    def nav_first(self):
        el = self._nav()
        root = el.find_elements_by_tag_name("li")[0]
        return root

    def nav_current(self):
        el = self._nav()
        return el.find_elements_by_css_selector("li.active")[0]

    def rows_click(self, rows, index):
        rows[index].click()
        WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "div.form-sheet")))

    def table_rows(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "tr.table-row")

    def table_rows_empty(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "tr.table-row-empty")


def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")
    except WebDriverException:
        pass