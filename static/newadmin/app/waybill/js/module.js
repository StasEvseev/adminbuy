/**
 * Created by user on 29.07.15.
 */

angular.module("waybill.module", ['ui.router', 'core.controllers', 'waybill.service'])
.run(function($templateCache, $http) {
    $templateCache.put('InvoiceForm', $http.get("static/newadmin/app/waybill/template/form_.html"));
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
                    templateUrl: "static/newadmin/app/waybill/template/list_.html",
                    controller: "InvoiceListController"
                }
            }
        })

        .state('index.invoice_in.create', {
            url: '/create',
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/app/waybill/template/create_.html",
                    controller: "InvoiceCreateCntr"
                }
            }
        })

        .state('index.invoice_in.view', {
            url: '/:id',
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/app/waybill/template/read_.html",
                    controller: "InvoiceViewCntr"
                }
            },
            resolve: {
                items: function (waybillitems, $stateParams) {
                    return waybillitems.all($stateParams.id);
                },
                item: function (waybills, $stateParams) {
                    return waybills.getById(parseInt($stateParams.id));
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
                    templateUrl: "static/newadmin/app/waybill/template/read_create.html",
                    controller: "InvoiceEditCntr"
                }
            }
        })
})
.controller("InvoiceListController", function ($scope, $stateParams, $state, ngTableParams, waybills, $controller) {
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
        return waybills;
    };
})

.controller('InvoiceViewCntr', function ($scope, $state, $stateParams, waybills, item, items, pointSource, pointReceiver, receiver, Company) {

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
            waybills.delete_(id).then(function(){
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

.controller('InvoiceCreateCntr', function ($scope, $state, Form, waybills, pointsales, receivers, Company, $controller, $q, PointService, ReceiverService) {
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
        return waybills.create($scope.model);
    };

    $scope.goView = function() {
        return "index.invoice_in.view";
    };
})

.controller('InvoiceEditCntr', function($scope, $controller, $stateParams, $modal,
                                        waybills, item, items, pointSource, pointReceiver,
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
        return waybills.update(parseInt($stateParams.id), $scope.model);
    };

    $scope.openWindowSelect = function() {
        var modalInstance = $modal.open({
            template: '<div class="modal-header">' +
                          '<h3 class="modal-title">' + 'Товар из накладной' + '</h3>' +
                      '</div>' +
                      '<div class="modal-body">' +
                          '<span ng-cloak ng-hide="loadingFinish" class="spinner"><span us-spinner="{lines: 13, length: 5, width: 2, radius: 5}" class="ng-scope"><div class="spinner" role="progressbar" style="position: absolute; width: 0px; z-index: 2000000000; left: 50%; top: 50%;"><div style="position: absolute; top: -1px; opacity: 0.25; -webkit-animation: opacity-100-25-0-13 1s linear infinite; animation-duration: 1s; animation-timing-function: linear; animation-delay: initial; animation-iteration-count: infinite; animation-direction: initial; animation-fill-mode: initial; -webkit-animation-play-state: initial; animation-play-state: initial; animation-name: opacity-100-25-0-13;"><div style="position: absolute; width: 7px; height: 2px; -webkit-box-shadow: rgba(0, 0, 0, 0.0980392) 0px 0px 1px; -webkit-transform-origin: left 50% 0px; -webkit-transform: rotate(0deg) translate(5px, 0px); border-radius: 1px; background: rgb(0, 0, 0);"></div></div><div style="position: absolute; top: -1px; opacity: 0.25; -webkit-animation: opacity-100-25-1-13 1s linear infinite; animation-duration: 1s; animation-timing-function: linear; animation-delay: initial; animation-iteration-count: infinite; animation-direction: initial; animation-fill-mode: initial; -webkit-animation-play-state: initial; animation-play-state: initial; animation-name: opacity-100-25-1-13;"><div style="position: absolute; width: 7px; height: 2px; -webkit-box-shadow: rgba(0, 0, 0, 0.0980392) 0px 0px 1px; -webkit-transform-origin: left 50% 0px; -webkit-transform: rotate(27deg) translate(5px, 0px); border-radius: 1px; background: rgb(0, 0, 0);"></div></div><div style="position: absolute; top: -1px; opacity: 0.25; -webkit-animation: opacity-100-25-2-13 1s linear infinite; animation-duration: 1s; animation-timing-function: linear; animation-delay: initial; animation-iteration-count: infinite; animation-direction: initial; animation-fill-mode: initial; -webkit-animation-play-state: initial; animation-play-state: initial; animation-name: opacity-100-25-2-13;"><div style="position: absolute; width: 7px; height: 2px; -webkit-box-shadow: rgba(0, 0, 0, 0.0980392) 0px 0px 1px; -webkit-transform-origin: left 50% 0px; -webkit-transform: rotate(55deg) translate(5px, 0px); border-radius: 1px; background: rgb(0, 0, 0);"></div></div><div style="position: absolute; top: -1px; opacity: 0.25; -webkit-animation: opacity-100-25-3-13 1s linear infinite; animation-duration: 1s; animation-timing-function: linear; animation-delay: initial; animation-iteration-count: infinite; animation-direction: initial; animation-fill-mode: initial; -webkit-animation-play-state: initial; animation-play-state: initial; animation-name: opacity-100-25-3-13;"><div style="position: absolute; width: 7px; height: 2px; -webkit-box-shadow: rgba(0, 0, 0, 0.0980392) 0px 0px 1px; -webkit-transform-origin: left 50% 0px; -webkit-transform: rotate(83deg) translate(5px, 0px); border-radius: 1px; background: rgb(0, 0, 0);"></div></div><div style="position: absolute; top: -1px; opacity: 0.25; -webkit-animation: opacity-100-25-4-13 1s linear infinite; animation-duration: 1s; animation-timing-function: linear; animation-delay: initial; animation-iteration-count: infinite; animation-direction: initial; animation-fill-mode: initial; -webkit-animation-play-state: initial; animation-play-state: initial; animation-name: opacity-100-25-4-13;"><div style="position: absolute; width: 7px; height: 2px; -webkit-box-shadow: rgba(0, 0, 0, 0.0980392) 0px 0px 1px; -webkit-transform-origin: left 50% 0px; -webkit-transform: rotate(110deg) translate(5px, 0px); border-radius: 1px; background: rgb(0, 0, 0);"></div></div><div style="position: absolute; top: -1px; opacity: 0.25; -webkit-animation: opacity-100-25-5-13 1s linear infinite; animation-duration: 1s; animation-timing-function: linear; animation-delay: initial; animation-iteration-count: infinite; animation-direction: initial; animation-fill-mode: initial; -webkit-animation-play-state: initial; animation-play-state: initial; animation-name: opacity-100-25-5-13;"><div style="position: absolute; width: 7px; height: 2px; -webkit-box-shadow: rgba(0, 0, 0, 0.0980392) 0px 0px 1px; -webkit-transform-origin: left 50% 0px; -webkit-transform: rotate(138deg) translate(5px, 0px); border-radius: 1px; background: rgb(0, 0, 0);"></div></div><div style="position: absolute; top: -1px; opacity: 0.25; -webkit-animation: opacity-100-25-6-13 1s linear infinite; animation-duration: 1s; animation-timing-function: linear; animation-delay: initial; animation-iteration-count: infinite; animation-direction: initial; animation-fill-mode: initial; -webkit-animation-play-state: initial; animation-play-state: initial; animation-name: opacity-100-25-6-13;"><div style="position: absolute; width: 7px; height: 2px; -webkit-box-shadow: rgba(0, 0, 0, 0.0980392) 0px 0px 1px; -webkit-transform-origin: left 50% 0px; -webkit-transform: rotate(166deg) translate(5px, 0px); border-radius: 1px; background: rgb(0, 0, 0);"></div></div><div style="position: absolute; top: -1px; opacity: 0.25; -webkit-animation: opacity-100-25-7-13 1s linear infinite; animation-duration: 1s; animation-timing-function: linear; animation-delay: initial; animation-iteration-count: infinite; animation-direction: initial; animation-fill-mode: initial; -webkit-animation-play-state: initial; animation-play-state: initial; animation-name: opacity-100-25-7-13;"><div style="position: absolute; width: 7px; height: 2px; -webkit-box-shadow: rgba(0, 0, 0, 0.0980392) 0px 0px 1px; -webkit-transform-origin: left 50% 0px; -webkit-transform: rotate(193deg) translate(5px, 0px); border-radius: 1px; background: rgb(0, 0, 0);"></div></div><div style="position: absolute; top: -1px; opacity: 0.25; -webkit-animation: opacity-100-25-8-13 1s linear infinite; animation-duration: 1s; animation-timing-function: linear; animation-delay: initial; animation-iteration-count: infinite; animation-direction: initial; animation-fill-mode: initial; -webkit-animation-play-state: initial; animation-play-state: initial; animation-name: opacity-100-25-8-13;"><div style="position: absolute; width: 7px; height: 2px; -webkit-box-shadow: rgba(0, 0, 0, 0.0980392) 0px 0px 1px; -webkit-transform-origin: left 50% 0px; -webkit-transform: rotate(221deg) translate(5px, 0px); border-radius: 1px; background: rgb(0, 0, 0);"></div></div><div style="position: absolute; top: -1px; opacity: 0.25; -webkit-animation: opacity-100-25-9-13 1s linear infinite; animation-duration: 1s; animation-timing-function: linear; animation-delay: initial; animation-iteration-count: infinite; animation-direction: initial; animation-fill-mode: initial; -webkit-animation-play-state: initial; animation-play-state: initial; animation-name: opacity-100-25-9-13;"><div style="position: absolute; width: 7px; height: 2px; -webkit-box-shadow: rgba(0, 0, 0, 0.0980392) 0px 0px 1px; -webkit-transform-origin: left 50% 0px; -webkit-transform: rotate(249deg) translate(5px, 0px); border-radius: 1px; background: rgb(0, 0, 0);"></div></div><div style="position: absolute; top: -1px; opacity: 0.25; -webkit-animation: opacity-100-25-10-13 1s linear infinite; animation-duration: 1s; animation-timing-function: linear; animation-delay: initial; animation-iteration-count: infinite; animation-direction: initial; animation-fill-mode: initial; -webkit-animation-play-state: initial; animation-play-state: initial; animation-name: opacity-100-25-10-13;"><div style="position: absolute; width: 7px; height: 2px; -webkit-box-shadow: rgba(0, 0, 0, 0.0980392) 0px 0px 1px; -webkit-transform-origin: left 50% 0px; -webkit-transform: rotate(276deg) translate(5px, 0px); border-radius: 1px; background: rgb(0, 0, 0);"></div></div><div style="position: absolute; top: -1px; opacity: 0.25; -webkit-animation: opacity-100-25-11-13 1s linear infinite; animation-duration: 1s; animation-timing-function: linear; animation-delay: initial; animation-iteration-count: infinite; animation-direction: initial; animation-fill-mode: initial; -webkit-animation-play-state: initial; animation-play-state: initial; animation-name: opacity-100-25-11-13;"><div style="position: absolute; width: 7px; height: 2px; -webkit-box-shadow: rgba(0, 0, 0, 0.0980392) 0px 0px 1px; -webkit-transform-origin: left 50% 0px; -webkit-transform: rotate(304deg) translate(5px, 0px); border-radius: 1px; background: rgb(0, 0, 0);"></div></div><div style="position: absolute; top: -1px; opacity: 0.25; -webkit-animation: opacity-100-25-12-13 1s linear infinite; animation-duration: 1s; animation-timing-function: linear; animation-delay: initial; animation-iteration-count: infinite; animation-direction: initial; animation-fill-mode: initial; -webkit-animation-play-state: initial; animation-play-state: initial; animation-name: opacity-100-25-12-13;"><div style="position: absolute; width: 7px; height: 2px; -webkit-box-shadow: rgba(0, 0, 0, 0.0980392) 0px 0px 1px; -webkit-transform-origin: left 50% 0px; -webkit-transform: rotate(332deg) translate(5px, 0px); border-radius: 1px; background: rgb(0, 0, 0);"></div></div></div></span></span>' +
                          '<div class="form-group">' +
                              '<label for="exampleInputPassword1">Накладная</label>' +
                              '<dict-select-field on-select="invoiceSelect" ng-model="model.invoice" service="InvoiceService" lazy="true" can-create="false" can-edit="false" select="model.invoice_id" style="width: 100%" dng-required="true" dname="invoice">'+
                                  '<dict-select-field-match placeholder="Введите название накладной...">[[$select.selected.fullname]]</dict-select-field-match>'+
                                  '<dict-select-field-choices repeat="item in $items | propsFilter: {fullname: $select.search}">'+
                                      '<div ng-bind-html="item.fullname | highlight: $select.search"></div>'+
                                  '</dict-select-field-choices>'+
                              '</dict-select-field>'+
                          '</div>' +
                          '<div class="row">'+
                              '<div class="col-sm-12">'+
                                  '<table ng-table="tableParams" class="table table-hover table-bordered table-striped dataTable"'+
                                           'role="grid"'+
                                           'aria-describedby="example1_info" template-pagination="custom/pager">'+
                                      '<tr ng-repeat="item in $data">'+
                                          '<td width="30" style="text-align: left" header="\'ng-table/headers/checkbox.html\'">' +
                                              '<input type="checkbox" ng-model="checkboxes.items[item.id]" />' +
                                          '</td>' +
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
                          '</span>' +
                      '</div>' +
                      '<div class="modal-footer">' +
                      '<button class="btn btn-flat btn-primary" ng-click="ok()">Добавить</button>' +
                      '<button class="btn btn-flat btn-warning" ng-click="cancel()">Закрыть</button>' +
                      '</div>',
            controller: function($scope, ngTableParams, $modalInstance, arrayhelp, invoice_canon_items, excl_id, InvoiceService) {

                var items = [];

                $scope.ok = function () {
                    $modalInstance.close(
                        arrayhelp.getElemsByIds(_.keys($scope.checkboxes.items), items));
                };

                $scope.cancel = function () {
                    $modalInstance.dismiss('cancel');
                };

                $scope.InvoiceService = InvoiceService;

                $scope.invoiceSelect = function(item) {

                    $scope.item_id = item.id;

                    $scope.tableParams.reload();
                    $scope.loadingFinish = false;
                };

                $scope.tableParams = new ngTableParams({
                    page: 0,            // show first page
                    count: 200,          // count per page
                    sorting: {
                        name: 'asc'     // initial sorting
                    }
                },
                {
                    total: 0, // length of data
                    counts: [], // hide page counts control
                    getData: function ($defer, params) {
                        if($scope.item_id) {
                            invoice_canon_items.all($scope.item_id, excl_id).then(function(invoice_items_data) {
                                items = invoice_items_data.items;
                                params.total(invoice_items_data.count);
                                $scope.loadingFinish = true;

                                $defer.resolve(items);
                            })
                        } else {
                            $scope.loadingFinish = true;
                        }
                    }
                });

                $scope.checkboxes = { 'checked': false, items: {} };

                // watch for check all checkbox
                $scope.$watch('checkboxes.checked', function(value) {
                    angular.forEach(items, function(item) {
                        if (angular.isDefined(item.id)) {
                            $scope.checkboxes.items[item.id] = value;
                        }
                    });
                });

                // watch for data checkboxes
                $scope.$watch('checkboxes.items', function(values) {
                    if (!items) {
                        return;
                    }
                    var checked = 0, unchecked = 0,
                            total = items.length;
                    angular.forEach(items, function(item) {
                        checked   +=  ($scope.checkboxes.items[item.id]) || 0;
                        unchecked += (!$scope.checkboxes.items[item.id]) || 0;
                    });
                    if ((unchecked == 0) || (checked == 0)) {
                        $scope.checkboxes.checked = (checked == total);
                    }
                    // grayed checkbox
                    angular.element(document.getElementById("select_all")).prop("indeterminate", (checked != 0 && unchecked != 0));
        }, true);

            },
            backdrop: "static",
            size: "lg",
            resolve: {
                excl_id: function() {
                    return _.map($scope.items, function(item) { return item.good_id });
                }
            }
        });
        modalInstance.result.then(function (items) {
            $scope.items = $scope.items.concat(items);
        }, function () {
        });
    };
});