# coding: utf-8

from flask.ext.assets import Environment, Bundle
from webassets.filter.jinja2 import Jinja2
from config import API_LOCATION

__author__ = 'StasEvseev'


assets = Environment()

jquery_bundle = Bundle(
    'js/lib/jquery.js',
    'js/lib/jquery.ba-resize.min.js'
)

na_css_bundle = Bundle(
    'newadmin/css/main.css',
    'newadmin/css/AdminLTE.css',
    'newadmin/css/adminlte_extens.css',
    'newadmin/css/dataTables.bootstrap.css',
    'newadmin/css/skins/_all-skins.min.css', output='gen/na.css'
)

moment_bundle = Bundle(
    'js/lib/moment-with-locales.js',
)

icheck_bundle = Bundle('js/lib/icheck.min.js')
icheck_css_line_bundle = Bundle(
    'newadmin/css/line/_all.css',
    output='gen/line/_all.css',
)
icheck_css_minimal_bundle = Bundle(
    'newadmin/css/minimal/_all.css',
    output='gen/minimal/_all.css',
)
icheck_css_square_bundle = Bundle(
    'newadmin/css/square/_all.css',
    output='gen/square/_all.css',
)
icheck_css_flat_bundle = Bundle(
    'newadmin/css/flat/_all.css',
    output='gen/flat/_all.css',
)

qtip_js_bundle = Bundle('js/lib/jquery.qtip.min.js')
underscore_bundle = Bundle('js/lib/underscore-min.1.8.3.js')
angularjs_lib_bundle = Bundle(
    'js/lib/angular1.4.js',
    output='gen/angular1.4.js'
)
angularjs_utils_bundle = Bundle(
    'js/lib/angular-ui-router.js',
    'js/lib/angular-resource.min.js',
    'js/lib/angular-animate.min.js',
    'js/lib/angular-route.min.js',
    'js/lib/angular-sanitize.js',
    Bundle(
        'js/lib/angular-clock.js',
        'js/lib/rainbow.min.js',
    ),
    Bundle(
        'js/lib/scrollglue.js'
    ),
    Bundle(
        'js/lib/angu-fixed-header-table.js',
        'js/lib/fixed-header.js'
    ),
    Bundle(
        'js/lib/angular-hidScanner.js'
    ),
    'js/lib/angular-locale_ru-ru.js',
    output='gen/angularjs-utils.min.js'
)
angularjs_spin_bundle = Bundle(
    'js/lib/angular-spinner.min.js',
    'js/lib/spin.min.js', output='gen/spin.min.js'
)
angularjs_ui_bootstrap_bundle = Bundle('js/lib/ui-bootstrap-tpls-0.14.3.min.js')
ng_table_js_bundle = Bundle('js/lib/ng-table.min.js')
select_js_bundle = Bundle('js/lib/select.js')
NAjs_bundle = Bundle(
    'js/lib/voilab-angular-qtip.js',
    'js/lib/socket.io.min.js',
    'newadmin/js/app.js',
    'newadmin/js/demo.js',

    'newadmin/js/app/db.js',
    'newadmin/js/app/filters.js',
    'newadmin/js/app/form.js',
    'newadmin/js/app/myapp.js',
    'newadmin/js/app/ui.js',
    'newadmin/js/app/directive.js',
    'newadmin/js/app/core/utils.js',
    'newadmin/js/app/core/helpers.js',
    'newadmin/js/app/core/controllers.js',
    'newadmin/js/app/core/service.js',

    'newadmin/js/applications/mail/js/mails-service.js',
    'newadmin/js/applications/mail/js/module.js',

    'newadmin/js/applications/invoice/js/module.js',
    'newadmin/js/applications/invoice/js/service.js',

    'newadmin/js/applications/waybill/js/service.js',
    'newadmin/js/applications/waybill/js/module.js',

    'newadmin/js/applications/pointsale/js/pointsales-service.js',
    'newadmin/js/applications/pointsale/js/module.js',

    'newadmin/js/applications/provider/js/service.js',
    'newadmin/js/applications/provider/js/module.js',

    'newadmin/js/applications/commodity/js/service.js',
    'newadmin/js/applications/commodity/js/module.js',

    'newadmin/js/applications/good/js/service.js',
    'newadmin/js/applications/good/js/module.js',

    'newadmin/js/applications/collect/js/service.js',
    'newadmin/js/applications/collect/js/module.js',

    'newadmin/js/applications/acceptance/js/service.js',
    'newadmin/js/applications/acceptance/js/module.js',

    'newadmin/js/applications/receiver/js/receivers-service.js',
    'newadmin/js/applications/receiver/js/module.js',

    'newadmin/js/applications/user/js/users-service.js',
    'newadmin/js/applications/user/js/module.js',

    'newadmin/js/applications/session/js/module.js',
    'newadmin/js/applications/session/js/service.js',

    'newadmin/js/app/utils.js',
    'newadmin/js/app/application.js',
    'newadmin/js/app/user.js',
    'newadmin/js/app/auth/http.js',
    'newadmin/js/app/auth/ui.js',
    'newadmin/js/angular-indexed-db.js',
    'js/lib/counter.js',
    output='gen/myapp.min.js',
    filters=Jinja2(context={'api_location': API_LOCATION}),

)
toastrjs_bundle = Bundle('js/lib/toastr.min.js')
sw_bundle = Bundle('newadmin/js/serviceworkerinit.js')

ng_table_css_bundle = Bundle('css/lib/ng-table.min.css')
qtip_css_bundle = Bundle('css/lib/jquery.qtip.min.css')
select_css_bundle = Bundle('css/lib/select.css', 'css/lib/select2.css')
angularjs_utils_css_bundle = Bundle(
    'css/lib/angular-clock.css',
    Bundle('css/lib/fixed-header.css')
)

bundles = {
    'NAjs': NAjs_bundle,

    'NAcss': na_css_bundle,

    'jquery': jquery_bundle,

    'sw': sw_bundle,

    'icheck': icheck_bundle,
    'login_css': Bundle('newadmin/css/all.css', output='gen/login_css.css'),

    'DT_JS': Bundle(
        'js/lib/jquery.dataTables.js'
    ),
    'DT_CSS': Bundle(
        'css/lib/jquery.dataTables.css',
        'css/lib/jquery.dataTables_themeroller.css',
        output='gen/css/DT.css'
    ),
    'js_all': Bundle('main.js', output='gen/packed.js'),
    'css_all': Bundle('css/main.css', output='gen/css/main.css'),

    'underscore': underscore_bundle,

    'font-awesome-css': Bundle(
        'css/lib/font-awesome-4.1.0/css/font-awesome.min.css', output='gen/font-awesome-css.css'
    ),

    'selectize-css': Bundle('css/lib/selectize.default.css', output='gen/selectize-css.css'),

    'bootstrap-css': Bundle('css/lib/bootstrap.min.css', output='gen/bootstrap.min.css'),
    'bootstrap-js': Bundle('js/lib/bootstrap.min.js'),

    'ng-grid-css': Bundle('css/lib/ng-grid.css'),
    'ng-grid-js': Bundle('js/lib/ng-grid.debug.js'),

    'ng-table-css': ng_table_css_bundle,
    'ng-table-js': ng_table_js_bundle,

    'select-js': select_js_bundle,
    'select-css': select_css_bundle,

    'indexmail': Bundle('js/mail/indexmail.js'),
    'prices': Bundle('js/mail/prices.js'),

    'toastrcss': Bundle('css/lib/toastr.min.css', output='gen/toastr.min.css'),
    'toastrjs': toastrjs_bundle,

    'angularjs-utils-css': angularjs_utils_css_bundle,

    'angularjs-lib': angularjs_lib_bundle,
    'angularjs-utils': angularjs_utils_bundle,

    'angularjs-spin': angularjs_spin_bundle,

    'angularjs-ui-bootstrap-old': Bundle(
        'js/lib/ui-bootstrap-tpls-0.11.2.min.js'
    ),

    'angularjs-ui-bootstrap': angularjs_ui_bootstrap_bundle,

    'bootbox': Bundle('js/lib/bootbox.min.js'),

    'chart_js': Bundle('js/lib/Chart.js'),

    'metisMenu_css': Bundle('css/lib/metisMenu.css'),

    'metisMenu_js': Bundle('js/lib/metisMenu.js'),

    'custom_dash': Bundle('css/custom/sb-admin.css'),

    'qtip_css': qtip_css_bundle,
    'qtip_js': qtip_js_bundle,

    'icheck_css_line_bundle': icheck_css_line_bundle,
    'icheck_css_flat_bundle': icheck_css_flat_bundle,
    'icheck_css_square_bundle': icheck_css_square_bundle,
    'icheck_css_minimal_bundle': icheck_css_minimal_bundle,


    'css_all_1': Bundle(
        ng_table_css_bundle,
        qtip_css_bundle,
        select_css_bundle,
        angularjs_utils_css_bundle,

        # icheck_css_line_bundle,
        # icheck_css_flat_bundle,
        # icheck_css_square_bundle,
        # icheck_css_minimal_bundle,
        output='gen/css_all_1.css'
    ),

    'js_all_1': Bundle(
        jquery_bundle,
        moment_bundle,
        icheck_bundle,
        qtip_js_bundle,
        underscore_bundle,
        angularjs_lib_bundle,
        angularjs_utils_bundle,
        angularjs_spin_bundle,
        angularjs_ui_bootstrap_bundle,
        ng_table_js_bundle,
        select_js_bundle,
        NAjs_bundle,
        toastrjs_bundle,
        sw_bundle,
        output='gen/js_all_1.js'
    ),
}

assets.register(bundles)
