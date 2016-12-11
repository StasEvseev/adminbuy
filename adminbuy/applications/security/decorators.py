# coding: utf-8

from functools import wraps

from flask import g
from flask.ext.principal import RoleNeed, Permission, Identity
from flask.ext.restful import abort


__author__ = 'StasEvseev'


def roles_accepted2(*roles):
    """Decorator which specifies that a user must have at least one of the
    specified roles. Example::

        @app.route('/create_post')
        @roles_accepted('editor', 'author')
        def create_post():
            return 'Create Post'

    The current user must have either the `editor` role or `author` role in
    order to view the page.

    :param args: The possible roles.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            iden = Identity(g.user.id)
            for r in g.user.roles:
                iden.provides.add(RoleNeed(r.name))
            g.identity = iden
            perm = Permission(*[RoleNeed(role) for role in roles])
            if perm.can():
                return fn(*args, **kwargs)
            abort(403, message=u"Недостаточно прав!")
        return decorated_view
    return wrapper
