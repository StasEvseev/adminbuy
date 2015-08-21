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

    var id = $stateParams.id;
    $scope.model = {};
    $scope.item = item;
    $scope.items = items;

    $scope.model.pointSource = pointSource;
    $scope.model.pointReceiver = pointReceiver;
    $scope.model.receiver = receiver;

    $scope.edit = function() {
        $state.go('index.invoice_in.view.edit', {id: $stateParams.id});
    };

    $scope.delete_ = function() {
        if (confirm("Вы действительно хотите удалить запись?")) {
            invoices.delete_(id).then(function(){
                $state.go("index.invoice_in.list");
            });
        }
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

    $scope.saveToServer = function() {
        return invoices.create($scope.model);
    };

    $scope.goView = function() {
        return "index.invoice_in.view";
    };
})

.controller('InvoiceEditCntr', function($scope, $controller, $stateParams, $modal,
                                        invoices, item, items, pointSource, pointReceiver,
                                        receiver) {
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

    $scope.saveToServer = function() {
        return invoices.update(parseInt($stateParams.id), $scope.model);
    };

    $scope.openWindowSelect = function() {
        var modalInstance = $modal.open({
            template: '<div class="modal-header">' +
                          '<h3 class="modal-title">' + 'Товар из накладной' + '</h3>' +
                      '</div>' +
                      '<div class="modal-body">' +
                          '<div class="form-group">' +
                              '<label for="exampleInputPassword1">Торговая точка отправитель</label>' +
                              '<dict-select-field ng-model="model.pointSource" service="PointService" lazy="true" select="model.pointsale_from_id" style="width: 100%" dng-required="true" dname="pointsale_from">'+
                                  '<dict-select-field-match placeholder="Введите название...">[[$select.selected.name]]</dict-select-field-match>'+
                                  '<dict-select-field-choices repeat="item in $items | propsFilter: {name: $select.search}">'+
                                      '<div ng-bind-html="item.name | highlight: $select.search"></div>'+
                                  '</dict-select-field-choices>'+
                              '</dict-select-field>'+
                          '</div>' +
                          '<div class="row">'+
                              '<div class="col-sm-12">'+
                                  '<table ng-table="tableParams" class="table table-hover table-bordered table-striped dataTable"'+
                                           'role="grid"'+
                                           'aria-describedby="example1_info" template-pagination="custom/pager">'+
                                      '<tr ng-repeat="item in $data">'+
                                          '<td data-title="\'Наименование\'" sortable="\'name\'">'+
                                                '[[ item.name ]]'+
                                          '</td>'+
                                          '<td data-title="\'Номер\'" sortable="\'number\'">'+
                                                '[[ item.number ]]'+
                                          '</td>'+

                                          '<td data-title="\'Получатель\'" sortable="\'pointsale\'">'+
                                                '[[ item.pointsale ]]'+
                                          '</td>'+

                                          '<td data-title="\'Отправитель\'" sortable="\'pointsale_from\'">'+
                                                '[[ item.pointsale_from ]]'+
                                          '</td>'+
                                      '</tr>' +
                                  '</table>' +
                              '</div>' +
                          '</div>'+
                      '</div>' +
                      '<div class="modal-footer">' +
                      '<button class="btn btn-flat btn-primary" ng-click="ok()">Сохранить</button>' +
                      '<button class="btn btn-flat btn-warning" ng-click="cancel()">Закрыть</button>' +
                      '</div>',
            controller: function($scope, items, ngTableParams) {

                $scope.tableParams = new ngTableParams({
                    page: $scope.page,            // show first page
                    count: 100,          // count per page
                    sorting: {
                        name: 'asc'     // initial sorting
                    }
                },
                {
                    total: 0, // length of data
                    counts: [], // hide page counts control
                    getData: function ($defer, params) {
                        // use build-in angular filter
                        var orig_page_func = params.page;
//                        params.page = function (arg) {
//                            if (angular.isDefined(arg)) {
//                                $state.go($scope.goList(), {filter: $scope.searchText, page: arg})
//                            } else {
//                                return orig_page_func();
//                            }
//                        };

                        $scope.loadingFinish = false;


                            $defer.resolve(items);


//                        $scope.getService().filter($scope.searchText, $scope.page, params.count()).then(
//                            function (data) {
//                                $defer.resolve(data);
//                                params.total($scope.getService().count());
//                                $scope.loadingFinish = true;
//                            });
                    }
                });
            },
            size: "lg",
            resolve: {
                items: function(invoice_canon_items) {
                    return invoice_canon_items.all(2);
                }
            }
        });
        modalInstance.result.then(function (model) {

        }, function () {

        });
        console.log("OPEN")
    };
});