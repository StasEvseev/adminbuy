angular.module("waybill.module", ['ui.router', 'core.controllers', 'waybill.service'])

.run(function($templateCache, $http) {
    $templateCache.put('InvoiceInForm', $http.get("/static/newadmin/js/applications/waybill/template/form_.html"));

    $templateCache.put("InvoiceSelectGood", $http.get("/static/newadmin/js/applications/waybill/template/selectgood.html"));
})

.config(function($stateProvider) {
    $stateProvider.state('index.invoice_in', {
            data: {
                 roles: ['user']
            },
            abstract: true,
            url: '/invoice_in'
        })

        .state('index.invoice_in.bulk', {
            url: '/create_bulk?from_pointsale_id&to_pointsale_ids&invoice_from',
            views: {
                'content@index': {
                    templateUrl: "/static/newadmin/js/applications/waybill/template/page_bulk.html",
                    controller: function($scope, $controller, $state, $modal, frompointsale, topointsale, invoice_items, waybills) {
                        $controller('InvoiceInCreateCntr', {$scope: $scope});

                        if(frompointsale) {
                            $scope.model.pointSource = frompointsale;
                            $scope.model.pointsale_from_id = frompointsale.id;
                        }
                        if(topointsale) {
                            $scope.model.pointReceiver = topointsale;
                        }
                        if(invoice_items) {
                            $scope.model.items = invoice_items;
                        } else {
                            $scope.model.items = [];
                        }

                        $scope.saveToServer = function() {
                            return waybills.createBulk($scope.model);
                        };

                        $scope._goAfterSave = function(id) {
                            $state.go("index.invoice_in.list");
                        };

                        $scope._doFailSave = function() {
                            toastr.error(resp.data.message, "Ошибка!!!");
                        };

                        $scope.removeRow = function(row) {
                            if (confirm("Вы действительно хотите удалить запись из накладной?")) {
                                $scope.model.items = _.without($scope.model.items, row);
                            }
                        };

                        $scope.openWindowSelect = function() {
                            var modalInstance = $modal.open({
                                templateUrl: 'InvoiceSelectGood',
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
                                        if ((unchecked === 0) || (checked === 0)) {
                                            $scope.checkboxes.checked = (checked === total);
                                        }
                                        // grayed checkbox
                                        angular.element(document.getElementById("select_all")).prop("indeterminate", (checked !== 0 && unchecked !== 0));
                            }, true);

                                },
                                backdrop: "static",
                                size: "lg",
                                resolve: {
                                    excl_id: function() {
                                        return _.map($scope.model.items, function(item) { return item.good_id });
                                    }
                                }
                            });
                            modalInstance.result.then(function (items) {
                                items = _.map(items, function(item) {
                                    item.count = null;
                                    return item;
                                });
                                $scope.model.items = $scope.model.items.concat(items);
                            }, function () {
                            });
                        }
                    }
                }
            },
            resolve: {
                frompointsale: function(pointsales, $stateParams) {
                    if($stateParams.from_pointsale_id) {
                        return pointsales.getById(parseInt($stateParams.from_pointsale_id));
                    }
                },
                topointsale: function(pointsales, $stateParams) {
                    if($stateParams.to_pointsale_ids) {
                        return pointsales.getByIds($stateParams.to_pointsale_ids).then(function(resp) {return resp.items});
                    }
                },
                invoice_items: function(invoice_canon_items, $stateParams) {
                    if($stateParams.invoice_from) {
                        return invoice_canon_items.all($stateParams.invoice_from).then(function(resp) {return resp.items;});
                    }
                }
            }
        })

        .state('index.invoice_in.list', {
            url: "?filter&page",
            views: {
                'content@index': {
                    templateUrl: "/static/newadmin/js/applications/waybill/template/list_.html",
                    controller: "InvoiceInListController"
                }
            }
        })

        .state('index.invoice_in.create', {
            url: '/create',
            views: {
                'content@index': {
                    templateUrl: "/static/newadmin/js/applications/waybill/template/create_.html",
                    controller: "InvoiceInCreateCntr"
                }
            }
        })

        .state('index.invoice_in.view', {
            url: '/:id',
            views: {
                'content@index': {
                    templateUrl: "/static/newadmin/js/applications/waybill/template/read_.html",
                    controller: "InvoiceInViewCntr"
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
                    templateUrl: "/static/newadmin/js/applications/waybill/template/read_create.html",
                    controller: "InvoiceInEditCntr"
                }
            }
        })
})
.controller("InvoiceInListController", function ($scope, $stateParams, $state, ngTableParams, waybills, waybillprint, $controller) {
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

    $scope.createBulk = function() {
        $state.go("index.invoice_in.bulk");
    };

    $scope.printBulk = function() {

        var ids = _.map(_.filter(_.pairs($scope.checkboxes.items), function(item) {
            return item[1];
        }), function(item) {
            return parseInt(item[0]);
        });

        waybillprint.printBulk(ids).then(function(resp) {
            var url = resp.data.link;
            window.open(url, "_target");
        })
    };


    $scope.checkboxes = { 'checked': false, items: {} };

    // watch for check all checkbox
    $scope.$watch('checkboxes.checked', function(value) {
        var items = $scope.tableParams.data;
        angular.forEach(items, function(item) {
            if (angular.isDefined(item.id)) {
                $scope.checkboxes.items[item.id] = value;
            }
        });
    });

    // watch for data checkboxes
    $scope.$watch('checkboxes.items', function(values) {
        var items = $scope.tableParams.data;
        if (!items) {
            return;
        }
        var checked = 0, unchecked = 0,
                total = items.length;
        angular.forEach(items, function(item) {
            checked   +=  ($scope.checkboxes.items[item.id]) || 0;
            unchecked += (!$scope.checkboxes.items[item.id]) || 0;
        });
        if ((unchecked === 0) || (checked === 0)) {
            $scope.checkboxes.checked = (checked === total);
        }
        // grayed checkbox
        angular.element(document.getElementById("select_all")).prop("indeterminate", (checked !== 0 && unchecked !== 0));
    }, true);
})

.controller('InvoiceInViewCntr', function ($scope, $state, $stateParams, waybillstatus, waybills, waybillprint, item, items,
                                           pointSource, pointReceiver, receiver, Company) {

    var id = $stateParams.id;
    $scope.model = item;
    $scope.item = item;
    $scope.items = items;
    $scope.loadingFinish = true;

    $scope.model.pointSource = pointSource;
    $scope.model.pointReceiver = pointReceiver;
    $scope.model.receiver = receiver;

    $scope.toStatus = function(number) {
        if(number === 4) {
            if(confirm("Вы переводите накладную в финальный статус (когда товар уже должен быть доставлен). " +
                "Внимание! Операция необратимая.")){
                doIt();
            }
        } else {
            doIt();
        }

        function doIt(){
            $scope.loadingFinish = false;
            waybillstatus.doStatus($scope.model.id, number).then(function() {
                $state.go('index.invoice_in.view', {id: $scope.model.id}, {reload: 'index.invoice_in.view'}).then(function() {
                    $scope.loadingFinish = true;
                });
            });
        }
    };

    $scope.print = function() {
        waybillprint.print(id).then(function(resp) {
            var url = resp.data.link;
            window.open(url, "_target");
        })
    };

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

    $scope.price_item = function (row) {
        return $scope.model.type === 1 ? row.good.price.price_retail : row.good.price.price_gross;
    };

    $scope.sum_item = function (row) {
        var price = $scope.price_item(row);
        return row.count * price;
    };

    $scope.getTotal = function () {
        var total = 0;
        for (var i = 0; i < $scope.items.length; i++) {
            var product = $scope.items[i];
            var price = $scope.price_item(product);
            // var price = $scope.model.type === 1 ? product.good.price.price_retail : product.good.price.price_gross;
            total += (product.count * price);
        }
        return total;
    }
})

.controller('InvoiceInCreateCntr', function ($scope, $state, Form, waybills, pointsales, receivers,
                                             Company, $controller, $q, PointService, ReceiverService) {
    $controller('BaseCreateController', {$scope: $scope});

    $scope.model.typeRec = 1;
    $scope.model.type = 1;

    $scope.nameInvoice = Company.nameInvoice();

    $scope.goList = function() {
        return 'index.invoice_in.list';
    };

    $scope.select = function(date) {
      // here you will get updated date
        $scope.model.date = moment(date).format('YYYY-MM-DD');
    };

    $scope.PointService = PointService;
    $scope.ReceiverService = ReceiverService;

    $scope.today = function() {
        $scope.model.date = moment().format('YYYY-MM-DD');
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
        if(!$scope.editForm) {
            $scope.status.opened = true;
        }
    };
    $scope.status = {
        opened: false
    };
    $scope.dateOptions = {
        'starting-day': 1
    };

    $scope.saveToServer = function() {
        return waybills.create($scope.model);
    };

    $scope.goView = function() {
        return "index.invoice_in.view";
    };
})

.controller('InvoiceInEditCntr', function($scope, $state, $controller, $stateParams, $modal,
                                        waybills, item, items, pointSource, pointReceiver,
                                        receiver) {
    $controller('InvoiceInCreateCntr', {$scope: $scope});

    $scope.item = angular.copy(item);
    $scope.model = $scope.item;
    $scope.model.items = angular.copy(items);
    $scope.model.pointSource = pointSource;
    $scope.model.pointReceiver = pointReceiver;
    $scope.model.receiver = receiver;

    $scope.tableEdit = $scope.model.status === 2;
    $scope.editForm = !(!$scope.model.status || $scope.model.status === 1);

    $scope.select = function(date) {
      // here you will get updated date
        $scope.model.date = moment(date).format('YYYY-MM-DD');
    };

    $scope.removeRow = function(row) {
        if (confirm("Вы действительно хотите удалить запись из накладной?")) {
            $scope.model.items = _.without($scope.model.items, row);
        }
    };

    $scope.goList = function() {
        return 'index.invoice_in.list';
    };

    $scope._goAfterSave = function(id) {
        $state.go($scope.goView(), {id: id}, {reload: 'index.invoice_in.view'});
    };

    $scope.saveToServer = function() {
        return waybills.update(parseInt($stateParams.id), $scope.model);
    };

    $scope.openWindowSelect = function() {
        var modalInstance = $modal.open({
            templateUrl: "/static/newadmin/js/applications/waybill/template/w_add_from_invoice.html",
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
                    if ((unchecked === 0) || (checked === 0)) {
                        $scope.checkboxes.checked = (checked === total);
                    }
                    // grayed checkbox
                    angular.element(document.getElementById("select_all")).prop("indeterminate", (checked !== 0 && unchecked !== 0));
        }, true);

            },
            backdrop: "static",
            size: "lg",
            resolve: {
                excl_id: function() {
                    return _.map($scope.model.items, function(item) { return item.good_id });
                }
            }
        });
        modalInstance.result.then(function (items) {
            items = _.map(items, function(item) {
                item.count = null;
                return item;
            });
            $scope.model.items = $scope.model.items.concat(items);
        }, function () {
        });
    };
});