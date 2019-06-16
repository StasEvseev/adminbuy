
console.log('invoce_return');
angular.module('invoice_return.module', ['ui.router', 'core.controllers', 'pointsales.service']).constant('InvoiceReturnConfig', {
    name: "Возвратные накладные",
    // formname: "InvoiceForm"
})


.config(function($stateProvider) {
    $stateProvider.state('index.invoice_return', {
            data: {
                 roles: ['user']
            },
            abstract: true,
            url: '/invoice_return'
        })
        .state('index.invoice_return.list', {
            url: "?filter&page",
            views: {
                'content@index': {
                    templateUrl: "/static/newadmin/js/applications/invoice_return/template/list.html",
                    controller: "InvoiceReturnListCntr"
                }
            }
        })
        .state('index.invoice_return.create', {
            url: '/create',
            views: {
                'content@index': {
                    templateUrl: "/static/newadmin/js/applications/invoice_return/template/create.html",
                    controller: "InvoiceReturnCreateCntr"
                }
            }
        })
        .state('index.invoice_return.view', {
            url: "/:id",
            views: {
                'content@index': {
                    templateUrl: "/static/newadmin/js/applications/invoice_return/template/view.html",
                    controller: "InvoiceReturnViewCntr"
                }
            },
            resolve: {
                item: function(invoices_return, $stateParams) {
                    return invoices_return.getById(parseInt($stateParams.id))
                },
                items: function(invoices_return, $stateParams) {
                    return invoices_return.getItems(parseInt($stateParams.id));
                },
                // pointcentral: function(pointsales) {
                //     return pointsales.getCentralPoint();
                // },
                // pointslave: function(pointsales) {
                //     return pointsales.getSlavePoint();
                // }
            }
        })
        .state('index.invoice_return.view.edit', {
            url: "/edit",
            views: {
                'content@index': {
                    templateUrl: "/static/newadmin/js/applications/invoice_return/template/edit.html",
                    controller: "InvoiceReturnEditCntr"
                }
            },
            resolve: {
                item: function(invoices_return, $stateParams) {
                    return invoices_return.getById(parseInt($stateParams.id))
                },
                items: function(invoices_return, $stateParams) {
                    return invoices_return.getItems(parseInt($stateParams.id));
                },
            }
        })
})

.controller("InvoiceReturnListCntr", function($scope, $controller, InvoiceReturnConfig, invoices_return) {
    $controller('BaseListController', {$scope: $scope});
    $scope.name_head = InvoiceReturnConfig.name;

    $scope.goCreate = function() {
        return "index.invoice_return.create";
    };

    $scope.goView = function() {
        return "index.invoice_return.view";
    };

    $scope.goList = function() {
        return "index.invoice_return.list";
    };

    $scope.getService = function() {
        return invoices_return;
    };
})

.controller("InvoiceReturnCreateCntr", function($scope, $controller, invoices, InvoiceReturnConfig) {
    $controller('BaseCreateController', {$scope: $scope});
    $scope.name_head = InvoiceReturnConfig.name;

    // $scope.formname =  InvoiceReturnConfig.formname;

    $scope.saveToServer = function() {
        return invoices.create($scope.model);
    };

    $scope.goView = function() {
        return "index.invoice_return.view";
    };
})

.controller("InvoiceReturnEditCntr", function($scope, $controller, $state, item, items, invoices_return, InvoiceReturnConfig) {
    $controller('BaseCreateController', {$scope: $scope});

    $scope.name_head = InvoiceReturnConfig.name;
    // $scope.formname =  InvoiceReturnConfig.formname;

    $scope.goView = function() {
        return "index.invoice_return.view";
    };

    $scope.model = item;
    $scope.model.items = items;

    $scope.loadingFinish = true;

    $scope._goCancel = function() {
        $state.go("index.invoice_return.view", {mailId: $scope.item.id});
    };

    $scope.save = function() {
        $scope.loadingFinish = false;

        invoices_return.saveAmountFromInvoice($scope.model.id, $scope.model.items).then(function() {

            $state.go("index.invoice_return.view", {mailId: $scope.model.id}, {reload: 'index.invoice_return.view'}).then(function() {
                $scope.loadingFinish = true;
            });
//            toastr.success("Можно переходить к следующему действию " +
//                "<a href='/admin2#/invoice_in/create_bulk?from_pointsale_id=1&to_pointsale_ids=%5B8,7,6,5,2%5D&invoice_from="+ $scope.model.id +"'>плиии!!</a>.", "Цены сохранены!");

        }, function(resp) {
            toastr.error(resp.data.message, "Ошибка при сохранении!");
            $scope.loadingFinish = true;
        });
    };
})

.controller("InvoiceReturnViewCntr", function($scope, $stateParams, $state, InvoiceReturnConfig, invoices_return, item, items) {
    $scope.name_head = InvoiceReturnConfig.name;

    $scope.loadingFinish = true;

    var id = $stateParams.id;
    $scope.model = item;
    $scope.model.items = items;

    $scope.edit = function() {
        $scope.loadingFinish = false;
        $state.go('index.invoice_return.view.edit', {id: id}).then(function() {
            $scope.loadingFinish = true;
        });

    };

    $scope.printEmpty = function() {
        invoices_return.print(id).then(function(data) {
            const blob = new Blob([data.data], { type: data.headers('content-type') });
            var link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = 'report_empty_' + id + '.xlsx';
            link.click();
        })
    };

    // $scope.createBulk = function() {
    //     $scope.loadingFinish = false;
    //     var from_pointsale_id = '', to_pointsale_ids = '';
    //     if (pointcentral) {
    //         from_pointsale_id = pointcentral.id;
    //     }
    //     if (pointslave) {
    //         to_pointsale_ids = _.map(pointslave, function(item) {return item.id});
    //         to_pointsale_ids = "[" + to_pointsale_ids.join(",") + "]";
    //     }
    //     $state.go('index.invoice_in.bulk', {
    //         from_pointsale_id: from_pointsale_id,
    //         to_pointsale_ids: to_pointsale_ids,
    //         invoice_from: id}).then(function() {
    //         $scope.loadingFinish = true;
    //     });
    // };

    $scope.delete_ = function() {
        if (confirm("Вы действительно хотите удалить запись?")) {
            invoices_return.delete_(id).then(function(){
                $state.go("index.invoice_return.list");
            });
        }
    };
});