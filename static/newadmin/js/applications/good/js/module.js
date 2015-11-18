/**
 * Created by user on 17.08.15.
 */

angular.module('good.module', ['core.controllers']).constant('configGood', {
    name: "Товар",
    formname: "GoodForm"
})

.run(function($templateCache, $http) {
    $templateCache.put("GoodForm", $http.get("static/newadmin/js/applications/good/template/form.html"));
})


.config(function($stateProvider) {
    $stateProvider.state('index.good', {
            data: {
                 roles: ['user']
            },
            abstract: true,
            url: '/good'
        })
        .state('index.good.list', {
            url: "?filter&page",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/good/template/list.html",
                    controller: "GoodListCntr"
                }
            }
        })
        .state('index.good.create', {
            url: '/create',
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/good/template/create.html",
                    controller: "GoodCreateCntr"
                }
            }
        })
        .state('index.good.view', {
            url: "/:id",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/good/template/view.html",
                    controller: "GoodViewCntr"
                }
            },
            resolve: {
                item: function(goods, $stateParams) {
                    return goods.getById(parseInt($stateParams.id))
                }
            }
        })
        .state('index.good.view.edit', {
            url: "/edit",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/good/template/edit.html",
                    controller: "GoodEditCntr"
                }
            }
        })
})

.controller("GoodListCntr", function($scope, $controller, configGood, goods) {
    $controller('BaseListController', {$scope: $scope});
    $scope.name_head = configGood.name;

    $scope.goCreate = function() {
        return "index.good.create";
    };

    $scope.goView = function() {
        return "index.good.view";
    };

    $scope.goList = function() {
        return "index.good.list";
    };

    $scope.getService = function() {
        return goods;
    };
})

.controller("GoodCreateCntr", function($scope, $controller, goods, configGood, CommodityService) {
    $controller('BaseCreateController', {$scope: $scope});
    $scope.name_head = configGood.name;

    $scope.formname =  configGood.formname;
    $scope.CommodityService = CommodityService;

    $scope.saveToServer = function() {
        return goods.create($scope.model);
    };

    $scope.goView = function() {
        return "index.good.view";
    };
})

.controller("GoodEditCntr", function($scope, $controller, goods, item, configGood, CommodityService) {
    $controller('BaseCreateController', {$scope: $scope});
    $scope.model = item;
    $scope.name_head = configGood.name;
    $scope.formname =  configGood.formname;
    $scope.CommodityService = CommodityService;

    $scope.saveToServer = function() {
        return goods.update($scope.model.id, $scope.model);
    };

    $scope.goView = function() {
        return "index.good.view";
    };
})

.controller("GoodViewCntr", function($scope, $stateParams, $state, goods, configGood, item) {
    $scope.name_head = configGood.name;

    var id = $stateParams.id;
    $scope.model = item;
    $scope.printBarCode = printBarCode;

    $scope.edit = function() {
        $state.go('index.good.view.edit', {id: id});
    };

    $scope.delete_ = function() {
        if (confirm("Вы действительно хотите удалить запись?")) {
            goods.delete_(id).then(function(){
                $state.go("index.good.list");
            });
        }
    };

    function printBarCode() {
        goods.printBarCode(id).then(function(resp) {
            var url = resp.data.link;
            window.open(url, "_target");
        }).catch(function(resp) {
            toastr.error(resp.data.message, "Ошибка!", {"closeButton": true, "progressBar": true})
        });
    }

});