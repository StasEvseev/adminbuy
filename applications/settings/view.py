#coding: utf-8
from angular.field import DecimalFieldBootstrap
from angular.urls import ResourceAngularUrl

from angular.view import ModelProjectAngularView
from applications.settings import ProfileCanon
from applications.settings.model import Profile


class SettingView(ModelProjectAngularView):
    resource_view = ResourceAngularUrl('/api', '/settings', ProfileCanon)
    model = Profile

    form_columns = {
        'rate_retail': DecimalFieldBootstrap(id='rate_retail', label=u"Коэффициент розницы", required=True),
        'rate_gross': DecimalFieldBootstrap(id='rate_gross', label=u"Коэффициент опта", required=True),
    }

    page = "test/singlerecord.html"

    grouping = (
        (
            (u"Коэффициенты", ('rate_retail', 'rate_gross')),
        ),
    )