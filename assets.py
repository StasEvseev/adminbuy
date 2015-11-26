# coding: utf-8

from flask.ext.assets import Environment, Bundle

__author__ = 'StasEvseev'


assets = Environment()

bundles = {
    'NAjs': Bundle(
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
        'js/lib/counter.js'

    , output='gen/myapp.min.js'),
    'NAcss': Bundle(
        'newadmin/css/main.css',
        'newadmin/css/AdminLTE.css',
        'newadmin/css/adminlte_extens.css',
        'newadmin/css/dataTables.bootstrap.css',
        'newadmin/css/skins/_all-skins.min.css'),

    'jquery': Bundle(
        'js/lib/jquery.js',
        'js/lib/jquery.ba-resize.min.js'
    ),

    'sw': Bundle('newadmin/js/serviceworkerinit.js'),

    'icheck': Bundle('js/lib/icheck.min.js'),
    'login_css': Bundle('newadmin/css/all.css'),

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

    'underscore': Bundle('js/lib/underscore-min.1.8.3.js'),

    'font-awesome-css': Bundle(
        'css/lib/font-awesome-4.1.0/css/font-awesome.min.css'),

    'selectize-css': Bundle('css/lib/selectize.default.css'),

    'bootstrap-css': Bundle('css/lib/bootstrap.min.css'),
    'bootstrap-js': Bundle('js/lib/bootstrap.min.js'),

    'ng-grid-css': Bundle('css/lib/ng-grid.css'),
    'ng-grid-js': Bundle('js/lib/ng-grid.debug.js'),

    'ng-table-css': Bundle('css/lib/ng-table.min.css'),
    'ng-table-js': Bundle('js/lib/ng-table.min.js'),

    'select-js': Bundle('js/lib/select.js'),
    'select-css': Bundle('css/lib/select.css',
                         'css/lib/select2.css'),

    'indexmail': Bundle('js/mail/indexmail.js'),
    'prices': Bundle('js/mail/prices.js'),

    'toastrcss': Bundle('css/lib/toastr.min.css'),
    'toastrjs': Bundle('js/lib/toastr.min.js'),

    'angularjs-utils-css': Bundle(
        'css/lib/angular-clock.css',
        Bundle('css/lib/fixed-header.css')
    ),

    'angularjs-lib': Bundle('js/lib/angular1.4.js'),
    'angularjs-utils': Bundle(
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
        'js/lib/angular-locale_ru-ru.js', output='gen/angularjs-utils.min.js'),

    'angularjs-spin': Bundle(
        'js/lib/angular-spinner.min.js',
        'js/lib/spin.min.js', output='gen/spin.min.js'
    ),

    # TODO: LEGACY

    # 'angularjs': Bundle('js/lib/angular.js',
    #                     'js/lib/angular-resource.min.js',
    #                     'js/lib/angular-animate.min.js',
    #                     'js/lib/angular-route.min.js',
    #                     'js/lib/angular-sanitize.js',
    #                     'js/lib/ng-breadcrumbs.js',
    #                     'js/lib/angular-spinner.min.js',
    #                     'js/lib/spin.min.js',
    #                     'js/lib/angular-locale_ru-ru.js',
    #                     'js/angular/number.js',
    #                     'js/angular/auth.js',
    #                     'js/angular/rest.js',
    #                     'js/angular/table.js',
    #                     'js/angular/filter.js',
    #                     'js/angular/params.js',
    #                     'js/angular/modalWindow.js',
    #                     'js/angular/elems.js',
    #
    #                     'js/bl/goodbl.js'
    #                     ),

    'angularjs-ui-bootstrap-old': Bundle(
        'js/lib/ui-bootstrap-tpls-0.11.2.min.js'),
    # 'angularjs-ui-bootstrap': Bundle('js/lib/ui-bootstrap-tpls-0.13.3.js'),
    'angularjs-ui-bootstrap': Bundle('js/lib/ui-bootstrap-tpls-0.14.3.min.js'),

    'bootbox': Bundle('js/lib/bootbox.min.js'),

    'chart_js': Bundle('js/lib/Chart.js'),

    'metisMenu_css': Bundle('css/lib/metisMenu.css'),

    'metisMenu_js': Bundle('js/lib/metisMenu.js'),

    'custom_dash': Bundle('css/custom/sb-admin.css'),
}

assets.register(bundles)