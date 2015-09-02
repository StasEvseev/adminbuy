/**
 * Created by user on 02.09.15.
 */

/**
 * Created by user on 14.08.15.
 */

angular.module('invoice.module', ['core.controllers']).constant('InvoiceConfig', {
    name: "Расходные накладные",
    formname: "InvoiceForm"
})

.run(function($templateCache, $http) {
    $templateCache.put("InvoiceForm", $http.get("static/newadmin/app/invoice/template/form.html"));
})


.config(function($stateProvider) {
    $stateProvider.state('index.invoice', {
            abstract: true,
            url: '/invoice'
        })
        .state('index.invoice.list', {
            url: "?filter&page",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/app/invoice/template/list.html",
                    controller: "InvoiceListCntr"
                }
            }
        })
        .state('index.invoice.create', {
            url: '/create',
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/app/invoice/template/create.html",
                    controller: "InvoiceCreateCntr"
                }
            }
        })
        .state('index.invoice.view', {
            url: "/:id",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/app/invoice/template/view.html",
                    controller: "InvoiceViewCntr"
                }
            },
            resolve: {
                item: function(invoices, $stateParams) {
                    return invoices.getById(parseInt($stateParams.id))
                },
                items: function(invoices, $stateParams) {
                    return invoices.getRowInvoiceIn(parseInt($stateParams.id));
                }
            }
        })
        .state('index.invoice.view.edit', {
            url: "/edit",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/app/invoice/template/edit.html",
                    controller: "InvoiceEditCntr"
                }
            }
        })
})

.controller("InvoiceListCntr", function($scope, $controller, InvoiceConfig, invoices) {
    $controller('BaseListController', {$scope: $scope});
    $scope.name_head = InvoiceConfig.name;

    $scope.goCreate = function() {
        return "index.invoice.create";
    };

    $scope.goView = function() {
        return "index.invoice.view";
    };

    $scope.goList = function() {
        return "index.invoice.list";
    };

    $scope.getService = function() {
        return invoices;
    };
})

.controller("InvoiceCreateCntr", function($scope, $controller, invoices, InvoiceConfig) {
    $controller('BaseCreateController', {$scope: $scope});
    $scope.name_head = InvoiceConfig.name;

    $scope.formname =  InvoiceConfig.formname;

    $scope.saveToServer = function() {
        return invoices.create($scope.model);
    };

    $scope.goView = function() {
        return "index.invoice.view";
    };
})

.controller("InvoiceEditCntr", function($scope, $controller, $state, item, items, invoices, InvoiceConfig) {
    $controller('BaseCreateController', {$scope: $scope});

    $scope.name_head = InvoiceConfig.name;
    $scope.formname =  InvoiceConfig.formname;

    $scope.goView = function() {
        return "index.invoice.view";
    };

    $scope.model = item;
    $scope.model.items = items;

    $scope.loadingFinish = true;

    $scope._goCancel = function() {
        $state.go("index.invoice.view", {mailId: $scope.item.id});
    };

    $scope.save = function() {
        $scope.loadingFinish = false;

        invoices.savePriceFromInvoice($scope.model.id, $scope.model.items).then(function() {
            toastr.success("Можно переходить к следующему действию " +
                "<a href='/admin2#/invoice_in/create_bulk?from_pointsale_id=1&to_pointsale_ids=%5B8,7,6,5,2%5D&invoice_from="+ $scope.model.id +"'>плиии!!</a>.", "Цены сохранены!");
            $scope.loadingFinish = true;
        }, function(resp) {
            toastr.error(resp.data.message, "Цены не сохранены!");
            $scope.loadingFinish = true;
        });
    };
})

.controller("InvoiceViewCntr", function($scope, $stateParams, $state, InvoiceConfig, invoices, item, items) {
   $scope.name_head = InvoiceConfig.name;

   var id = $stateParams.id;
    $scope.model = item;
    $scope.model.items = items;

    $scope.edit = function() {
        $state.go('index.invoice.view.edit', {id: id});
    };

    $scope.delete_ = function() {
        if (confirm("Вы действительно хотите удалить запись?")) {
            invoices.delete_(id).then(function(){
                $state.go("index.invoice.list");
            });
        }
    };
});