#coding: utf-8
import os


def path_to_template():
    from app import app
    return os.path.join(app.root_path, app.template_folder)


def path_to_cache(name):
    return os.path.join(path_to_template(), "test/_cache/" + name)


def pathrend_to_cache(name):
    return 'test/_cache/' + name