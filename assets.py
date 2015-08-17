#coding: utf-8

from flask.ext.assets import Environment, Bundle

assets = Environment()

bundles = {
    'NAjs': Bundle(
        'js/lib/socket.io.min.js',
        'newadmin/js/app.js',
        'newadmin/js/demo.js',

        'newadmin/js/app/filters.js',
        'newadmin/js/app/form.js',
        'newadmin/js/app/myapp.js',
        'newadmin/js/app/ui.js',
        'newadmin/js/app/directive.js',
        'newadmin/js/app/core/utils.js',
        'newadmin/js/app/core/helpers.js',
        'newadmin/js/app/core/controllers.js',
        'newadmin/js/app/core/service.js',
        'newadmin/js/app/mails/mails-service.js',

        'newadmin/js/app/invoices/invoices-service.js',
        'newadmin/js/app/invoices/module.js',

        'newadmin/js/app/pointsales/pointsales-service.js',
        'newadmin/js/app/pointsales/module.js',

        'template/newadmin/commodity/js/service.js',
        'template/newadmin/commodity/js/module.js',

        'newadmin/js/app/receivers/receivers-service.js',
        'newadmin/js/app/receivers/module.js',

        'newadmin/js/app/user/users-service.js',
        'newadmin/js/app/user/module.js',

        'newadmin/js/app/application.js',
        'newadmin/js/app/user.js',
        'newadmin/js/app/auth/http.js',
        'newadmin/js/app/auth/ui.js'

    , output='gen/myapp.min.js'),
    'NAcss': Bundle(
        'newadmin/css/main.css',
        'newadmin/css/AdminLTE.css',
        'newadmin/css/dataTables.bootstrap.css',
        'newadmin/css/skins/_all-skins.min.css'),

    'jquery': Bundle(
        'js/lib/jquery.js'
    ),

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

    'underscore': Bundle('js/lib/underscore-min.js'),

    'font-awesome-css': Bundle('css/lib/font-awesome-4.1.0/css/font-awesome.min.css'),

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

    'angularjs-lib': Bundle('js/lib/angular1.4.js'),
    'angularjs-utils': Bundle(
        'js/lib/angular-ui-router.js',
        'js/lib/angular-resource.min.js',
        'js/lib/angular-animate.min.js',
        'js/lib/angular-route.min.js',
        'js/lib/angular-sanitize.js',
        'js/lib/angular-locale_ru-ru.js', output='gen/angularjs-utils.min.js'),

    'angularjs-spin': Bundle(
        'js/lib/angular-spinner.min.js',
        'js/lib/spin.min.js', output='gen/spin.min.js'
    ),

    'angularjs': Bundle('js/lib/angular.js',
                        'js/lib/angular-resource.min.js',
                        'js/lib/angular-animate.min.js',
                        'js/lib/angular-route.min.js',
                        'js/lib/angular-sanitize.js',
                        'js/lib/ng-breadcrumbs.js',
                        'js/lib/angular-spinner.min.js',
                        'js/lib/spin.min.js',
                        'js/lib/angular-locale_ru-ru.js',
                        'js/angular/number.js',
                        'js/angular/auth.js',
                        'js/angular/rest.js',
                        'js/angular/table.js',
                        'js/angular/filter.js',
                        'js/angular/params.js',
                        'js/angular/modalWindow.js',
                        'js/angular/elems.js',

                        'js/bl/goodbl.js'
                        ),

    'angularjs-ui-bootstrap': Bundle('js/lib/ui-bootstrap-tpls-0.13.3.js'),

    'bootbox': Bundle('js/lib/bootbox.min.js'),

    # 'invoice_retail': Bundle('js/invoice.js'),



    # 'acceptance': Bundle('js/acceptance.js'),

    'chart_js': Bundle('js/lib/Chart.js'),

    'metisMenu_css': Bundle('css/lib/metisMenu.css'),

    'metisMenu_js': Bundle('js/lib/metisMenu.js'),

    'custom_dash': Bundle('css/custom/sb-admin.css'),

    # 'invoicemail': Bundle('js/invoice_mail.js'),

    # 'acceptance_invoice': Bundle('js/acceptance_invoice.js'),

    # 'pointselect': Bundle('js/pointselect.js'),

    'waybilllist': Bundle('waybill/js/waybilllist.js'),

    'acceptance': Bundle('acceptance/js/acceptance.js'),

    'mail': Bundle('js/mail/mail.js'),

    'good': Bundle('js/good/good.js')
}

assets.register(bundles)