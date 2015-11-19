var app = angular.module('myApp', ['ngRoute', 'ng-breadcrumbs', 'ngResource', 'ui.bootstrap', 'ngSanitize', 'ui.select', 'AuthModule', 'ngTable',
    'RestApp', 'TableHelper', 'FilterApp', 'Params', 'ModalApp', 'NumberApp', 'ngAnimate', 'GoodModule', 'ElemsModule', 'angularSpinner']);

app.controller("MainCtrl", function($scope, $route, $location, $routeParams, breadcrumbs) {
    $scope.$route = $route;
    $scope.$location = $location;
    $scope.$routeParams = $routeParams;
    $scope.breadcrumbs = breadcrumbs;
})

    .controller('MailMainCtrl', function($scope, MailItems, $location, breadcrumbs) {
        $scope.breadcrumbs = breadcrumbs;
        $scope.resource = MailItems.query;

        $scope.setSelected = function(item) {
            $location.path("/admin/mailview/" + item.id + "/edit-new");
            return
            if (item.invoice_id) {
                $location.path("/admin/mailview/" + item.id + "/edit");
            } else if (item.order_id) {
                location.href = "/admin/orderview/" + item.order_id + "/edit";
            } else {
                location.href = "/admin/returnview/" + item.return_id + "/edit";
            }

        };

        $scope.checkPost = function(event) {
            var btn = $(event.target);
            btn.button('loading');
            MailItems.query_check({}, function(data) {
                btn.button('reset');
                $scope.is_error = false;
                $scope.rel();
            }, function() {
                btn.button('reset');
                $scope.is_error = true;
            })
        };

        $scope.reload = function(text) {
            $scope.rel(text);
        };
    })

    .controller("EditCtrl2", function($scope, $routeParams, breadcrumbs, MailItem, PriceItems) {
        $scope.breadcrumbs = breadcrumbs;
        $scope.model = {};

        $scope.mail_id = $routeParams.id;

        MailItem.query({'id': $scope.mail_id}, function(data) {
            $scope.model = data;
            $scope.loadingFinish = true;
        });

        $scope.rashod = function(event, index) {
            var btn = $(event.target);
            btn.button('loading');

            MailItem.prep({'id': $scope.mail_id, 'index': index, 'action': 'R'},
            function(data) {
                btn.button('reset');
                $scope.is_error = false;
                if (data.id) {
                    location.href = "/admin/mailview/" + data.id + "/edit";
                }
            },
            function(data) {
                btn.button('reset');
                $scope.is_error = true;
                $scope.error_message = data.data.message;
            });
        };

        $scope.vosvrat = function(event, index) {
            var btn = $(event.target);
            btn.button('loading');

            MailItem.prep({'id': $scope.mail_id, 'index': index, 'action': 'V'},
            function(data) {
                btn.button('reset');
                $scope.is_error = false;
                if (data.return_id) {
                    location.href = "/admin/returnview/" + data.return_id + "/edit";
                }
            },
            function(data) {
                btn.button('reset');
                $scope.is_error = true;
                $scope.error_message = data.data.message;
            });
        };
    })

    .controller("EditCtrl", function($scope, $routeParams, breadcrumbs, InvoicePriceItems, PriceItems) {
        $scope.breadcrumbs = breadcrumbs;
        $scope.model = {};

        $scope.model.invoice_id = $routeParams.id;

        $scope.savePrice = function(event) {
            var btn = $(event.target);
            btn.button('loading');
            PriceItems.query({
                'data': {
                    'items': _.filter($scope.model.items, function(el) { return el['price_retail'] || el['price_gross'] }),
                    'invoice_id': $scope.model.invoice_id
                }
            }, function(resp) {
                $scope.model.is_success = true;
                $scope.model.is_error = false;
                btn.button('reset');

            }, function(resp) {
                $scope.model.is_success = false;
                $scope.model.is_error = true;
                btn.button('reset');
            });
        };

        InvoicePriceItems.query({ id: $scope.model.invoice_id }, function(data) {
            $scope.model.items = data.items;

            $scope.model.is_change = Boolean(_.find($scope.model.items, function(el) { return el['is_change'] }));
            $scope.loadingFinish = true;
        });
    })

    .config(function($routeProvider, $locationProvider) {
        $routeProvider
            .when('/admin/mailview', {
                templateUrl: '/___old/template/mail/main.html',
                controller: 'MailMainCtrl',
                label: 'Письма'
            })
            .when('/admin/mailview/:id/edit', {
                templateUrl: '/___old/template/mail/edit.html',
                controller: 'EditCtrl',
                label: 'Редактирование'
            })
            .when('/admin/mailview/:id/edit-new', {
                templateUrl: '/___old/template/mail/edit-new.html',
                controller: 'EditCtrl2',
                label: 'Редактирование2'
            })
            .otherwise({
                redirectTo: '/admin/mailview'
            });

        // configure html5 to get links working on jsfiddle
        $locationProvider.html5Mode(true);
    });