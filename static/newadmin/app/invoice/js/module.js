/**
 * Created by user on 29.07.15.
 */

angular.module("invoices.module", ['ui.router', 'core.controllers', 'invoices.service'])
.run(function($templateCache, $http) {
    $templateCache.put('InvoiceForm', $http.get("static/newadmin/app/invoice/template/form_.html"));
})
.config(function($stateProvider) {
    $stateProvider.state('index.invoice_in', {
            abstract: true,
            url: '/invoice_in'
        })
        .state('index.invoice_in.list', {
            url: "?filter&page",
            views: {

                'content@index': {
                    templateUrl: "static/newadmin/app/invoice/template/list_.html",
                    controller: "InvoiceListController"
                }
            }
        })

        .state('index.invoice_in.create', {
            url: '/create',
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/app/invoice/template/create_.html",
                    controller: "InvoiceCreateCntr"
                }
            }
        })

        .state('index.invoice_in.view', {
            url: '/:id',
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/app/invoice/template/read_.html",
                    controller: "InvoiceViewCntr"
                }
            },
            resolve: {
                items: function (invoicesitems, $stateParams) {
                    return invoicesitems.all($stateParams.id);
                },
                item: function (invoices, $stateParams) {
                    return invoices.getById(parseInt($stateParams.id));
                },
                pointSource: function(item, pointsales) {
                    return pointsales.getById(item.pointsale_from_id);
                },
                pointReceiver: function(item, pointsales) {
                    if(item.pointsale_id) {
                        return pointsales.getById(item.pointsale_id);
                    }
                },
                receiver: function(item, receivers) {
                    if (item.receiver_id) {
                        return receivers.getById(item.receiver_id);
                    }
                }
            }
        })

        .state('index.invoice_in.view.edit', {
            url: '/edit',
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/app/invoice/template/read_create.html",
                    controller: "InvoiceEditCntr"
                }
            }
        })
})
.controller("InvoiceListController", function ($scope, $stateParams, $state, ngTableParams, invoices, $controller) {
    $controller('BaseListController', {$scope: $scope});

    $scope.goList = function() {
        return 'index.invoice_in.list';
    };

    $scope.goCreate = function() {
        return "index.invoice_in.create";
    };

    $scope.goView = function() {
        return 'index.invoice_in.view';
    };

    $scope.getService = function() {
        return invoices;
    };
})

.controller('InvoiceViewCntr', function ($scope, $state, $stateParams, invoices, item, items, pointSource, pointReceiver, receiver, Company) {

    $scope.model = {};
    $scope.item = item;
    $scope.items = items;

    $scope.model.pointSource = pointSource;
    $scope.model.pointReceiver = pointReceiver;
    $scope.model.receiver = receiver;

    $scope.edit = function() {
        $state.go('index.invoice_in.view.edit', {id: $stateParams.id});
    };

    $scope.nameInvoice = Company.nameInvoice();

    $scope.getTotal = function () {
        var total = 0;
        for (var i = 0; i < $scope.items.length; i++) {
            var product = $scope.items[i];
            total += (product.count * product.good.price.price_retail);
        }
        return total;
    }
})

.controller('InvoiceCreateCntr', function ($scope, $state, Form, invoices, pointsales, receivers, Company, $controller, $q, PointService, ReceiverService) {
    $controller('BaseCreateController', {$scope: $scope});

    $scope.model.typeRec = 1;
    $scope.model.type = 1;

    $scope.nameInvoice = Company.nameInvoice();

    $scope.goList = function() {
        return 'index.invoice_in.list';
    };

    $scope.PointService = PointService;
    $scope.ReceiverService = ReceiverService;

    $scope.datepickers = {
        dt: false
    };
    $scope.today = function() {
        $scope.model.date = new Date();
    };

    $scope.today();

    $scope.showWeeks = true;
    $scope.toggleWeeks = function () {
        $scope.showWeeks = ! $scope.showWeeks;
    };

    $scope.clear = function () {
        $scope.model.date = null;
    };

    $scope.toggleMin = function() {
        $scope.minDate = ( $scope.minDate ) ? null : new Date();
    };
    $scope.toggleMin();

    $scope.open = function($event) {
        $scope.status.opened = true;
    };

    $scope.status = {
        opened: false
    };

    $scope.dateOptions = {
        'year-format': "'yy'",
        'starting-day': 1
    };

//        $scope.save = function(){
//            var form = Form.getForm();
//        };

    $scope.saveToServer = function() {
//        Form.getForm()
        return invoices.create($scope.model);
    };
})

.controller('InvoiceEditCntr', function($scope, $controller, item, items, pointSource, pointReceiver, receiver) {
    $controller('InvoiceCreateCntr', {$scope: $scope});

    $scope.item = angular.copy(item);
    $scope.model = $scope.item;
    $scope.items = angular.copy(items);
    $scope.model.pointSource = pointSource;
    $scope.model.pointReceiver = pointReceiver;
    $scope.model.receiver = receiver;

    $scope.goList = function() {
        return 'index.invoice_in.list';
    };

    $scope.openWindowSelect = function() {
        console.log("OPEN")
    };
});