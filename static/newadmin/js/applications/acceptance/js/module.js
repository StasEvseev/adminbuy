/**
 * Created by user on 02.09.15.
 */

/**
 * Created by user on 14.08.15.
 */

angular.module('acceptance.module', ['core.controllers', 'acceptance.service']).constant('AcceptanceConfig', {
    name: "Приемки",
    formname: "AcceptanceForm"
})

.run(function($templateCache, $http) {
    $templateCache.put("AcceptanceForm", $http.get("static/newadmin/js/applications/acceptance/template/form.html"));
})


.config(function($stateProvider) {
    $stateProvider.state('index.acceptance', {
            data: {
                 roles: ['user']
            },
            abstract: true,
            url: '/acceptance'
        })
        .state('index.acceptance.list', {
            url: "?filter&page",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/acceptance/template/list.html",
                    controller: "AcceptanceListCntr"
                }
            }
        })
        .state('index.acceptance.create', {
            url: '/create',
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/acceptance/template/create.html",
                    controller: "AcceptanceCreateCntr"
                }
            },
            resolve: {
                topointsale: function (pointsales, $stateParams) {
                    if ($stateParams.to_pointsale_id) {
                        return pointsales.getByIds($stateParams.to_pointsale_id).then(function (resp) {
                            return resp.items;
                        });
                    } else {
                        return pointsales.getCentralPoint();
                    }
                }
            }

        })
        .state('index.acceptance.view', {
            url: "/:id",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/acceptance/template/view.html",
                    controller: "AcceptanceViewCntr"
                }
            },
            resolve: {
                item: function(acceptances, $stateParams) {
                    return acceptances.getById(parseInt($stateParams.id))
                },
                items: function(acceptances, $stateParams) {
                    return acceptances.getItems(parseInt($stateParams.id));
                }
            }
        })
        .state('index.acceptance.view.edit', {
            url: "/edit",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/acceptance/template/edit.html",
                    controller: "AcceptanceEditCntr"
                }
            },
            resolve: {
                //items: function(acceptances, $stateParams) {
                //    return [];
                //    //return acceptances.getRowInvoiceIn(parseInt($stateParams.id));
                //}
            }
        })
})

.controller("AcceptanceListCntr", function($scope, $controller, AcceptanceConfig, acceptances) {
    $controller('BaseListController', {$scope: $scope});
    $scope.name_head = AcceptanceConfig.name;

    $scope.goCreate = function() {
        return "index.acceptance.create";
    };

    $scope.goView = function() {
        return "index.acceptance.view";
    };

    $scope.goList = function() {
        return "index.acceptance.list";
    };

    $scope.getService = function() {
        return acceptances;
    };
})

.controller("AcceptanceCreateCntr", function($scope, $controller, acceptances, AcceptanceConfig, ConfigWidgets, PointService,
                                             ProviderService, InvoiceService, topointsale) {
    $controller('BaseCreateController', {$scope: $scope});
    $scope.name_head = AcceptanceConfig.name;

    $scope.model.type = 1;

    $scope.model.pointsale = topointsale;

    $scope.formname =  AcceptanceConfig.formname;

    $scope.config_datepicker = ConfigWidgets.defaultConfigDatepicker($scope.model.date);

    $scope.PointService = PointService;
    $scope.ProviderService = ProviderService;
    $scope.InvoiceService = InvoiceService;

    $scope.saveToServer = function() {
        return acceptances.create($scope.model);
    };

    $scope.goView = function() {
        return "index.acceptance.view";
    };

    $scope.goList = function() {
        return "index.acceptance.list";
    };
})

.controller("AcceptanceEditCntr", function($scope, $controller, $state, item, items, acceptances, AcceptanceConfig) {
    $controller('BaseCreateController', {$scope: $scope});

    $scope.name_head = AcceptanceConfig.name;
    $scope.formname =  AcceptanceConfig.formname;

    $scope.goView = function() {
        return "index.acceptance.view";
    };

    $scope.model = item;
    $scope.model.items = items;

    $scope.loadingFinish = true;

    $scope._goCancel = function() {
        $state.go("index.acceptance.view", {mailId: $scope.item.id});
    };

    $scope.save = function() {
        $scope.loadingFinish = false;

        invoices.savePriceFromInvoice($scope.model.id, $scope.model.items).then(function() {

            $state.go("index.acceptance.view", {mailId: $scope.model.id}, {reload: 'index.acceptance.view'}).then(function() {
                $scope.loadingFinish = true;
            });

        }, function(resp) {
            toastr.error(resp.data.message, "Цены не сохранены!");
            $scope.loadingFinish = true;
        });
    };
})

.controller("AcceptanceViewCntr", function($scope, $stateParams, $state, acceptancestatus, AcceptanceConfig, invoices, item, items) {
    $scope.name_head = AcceptanceConfig.name;

    $scope.loadingFinish = true;

    var id = $stateParams.id;
    $scope.model = item;
    $scope.model.items = items;

    $scope.edit = function() {
        $scope.loadingFinish = false;
        $state.go('index.acceptance.view.edit', {id: id}).then(function() {
            $scope.loadingFinish = true;
        });

    };

    $scope.delete_ = function() {
        if (confirm("Вы действительно хотите удалить запись?")) {
            invoices.delete_(id).then(function(){
                $state.go("index.acceptance.list");
            });
        }
    };

    $scope.toStatus = function(number) {
        if(number == 3) {
            if(confirm("Вы переводите приемку в финальный статус (когда товар уже получен). " +
                "Внимание! Операция необратимая.")){
                doIt();
            }
        } else {
            doIt();
        }

        function doIt(){
            $scope.loadingFinish = false;
            acceptancestatus.doStatus($scope.model.id, number).then(function() {
                $state.go('index.acceptance.view', {id: $scope.model.id}, {reload: 'index.acceptance.view'}).then(function() {
                    $scope.loadingFinish = true;
                });
            });
        }
    };
});