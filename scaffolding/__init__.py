# coding: utf-8
import os

from jinja2 import Template

from config import PATH_TO_ANGULAR_APPS

__author__ = 'Stanislav'


def scaffold_angular(name):
    """
    Функция создает базовый каркас приложения на ангуляр.

    Проверяет наличие уже созданного каркаса.
    """

    name = name.lower()

    apps = map(lambda x: x.lower(), os.listdir(PATH_TO_ANGULAR_APPS))

    if name in apps:
        raise Exception(u"Angular application with name `%s` already exist." % name)

    name_cap = name.capitalize()
    name_service = name_cap + "Service"

    dir_to_app = os.path.join(PATH_TO_ANGULAR_APPS, name)
    dir_to_app_js = os.path.join(dir_to_app, "js")
    dir_to_app_template = os.path.join(dir_to_app, "template")

    os.mkdir(dir_to_app)
    os.mkdir(dir_to_app_js)
    os.mkdir(dir_to_app_template)

    print u"Command created directory `%s`" % dir_to_app
    print u"Command created directory `%s`" % dir_to_app_js
    print u"Command created directory `%s`" % dir_to_app_template

    files = [os.path.join(os.path.dirname(__file__), 'templates', 'module.js'),
             os.path.join(os.path.dirname(__file__), 'templates', 'service.js')]

    file_to = [os.path.join(dir_to_app_js, 'module.js'),
               os.path.join(dir_to_app_js, 'service.js')]

    for fl, fl_to in zip(files, file_to):
        with open(fl) as f, open(fl_to, 'w+') as f2:
            templ = Template(f.read().decode("utf-8"))
            f2.write(templ.render({
                'name': name, 'name_cap': name_cap,
                'name_service': name_service}).encode("utf-8"))
            print u"Command created file `%s`" % fl_to
