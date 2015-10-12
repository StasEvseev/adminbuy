# coding: utf-8
import types
from flask.ext.injector import FlaskInjector

__author__ = 'user'


def getInject():
    global inject
    return inject

inject = None

def register_injectors(app):
    inj_mods = []
    try:
        applications = __import__("applications")

        for ap_ in dir(applications):
            attr = getattr(applications, ap_)
            if _is_app(attr) and hasattr(attr, 'configure'):
                configure = getattr(attr, 'configure')
                inj_mods.append(configure)
    except ImportError:
        pass

    inj = FlaskInjector(app=app, modules=inj_mods)
    global inject
    inject = inj.injector

def _is_app(modul):
    return type(modul) == types.ModuleType