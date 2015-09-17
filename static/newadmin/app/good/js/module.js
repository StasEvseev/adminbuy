/**
 * Created by user on 17.08.15.
 */

angular.module('good.module', ['core.controllers']).constant('config', {
    name: "Товар",
    formname: "GoodForm"
})

.run(function($templateCache, $http) {
    $templateCache.put("GoodForm", $http.get("static/newadmin/app/good/template/form.html"));
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
                    templateUrl: "static/newadmin/app/good/template/list.html",
                    controller: "GoodListCntr"
                }
            }
        })
        .state('index.good.create', {
            url: '/create',
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/app/good/template/create.html",
                    controller: "GoodCreateCntr"
                }
            }
        })
        .state('index.good.view', {
            url: "/:id",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/app/good/template/view.html",
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
                    templateUrl: "static/newadmin/app/good/template/edit.html",
                    controller: "GoodEditCntr"
                }
            }
        })
})

.controller("GoodListCntr", function($scope, $controller, config, goods) {
    $controller('BaseListController', {$scope: $scope});
    $scope.name_head = config.name;

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

.controller("GoodCreateCntr", function($scope, $controller, goods, config, CommodityService) {
    $controller('BaseCreateController', {$scope: $scope});
    $scope.name_head = config.name;

    $scope.formname =  config.formname;
    $scope.CommodityService = CommodityService;

    $scope.saveToServer = function() {
        return goods.create($scope.model);
    };

    $scope.goView = function() {
        return "index.good.view";
    };
})

.controller("GoodEditCntr", function($scope, $controller, goods, item, config, CommodityService) {
    $controller('BaseCreateController', {$scope: $scope});
    $scope.model = item;
    $scope.name_head = config.name;
    $scope.formname =  config.formname;
    $scope.CommodityService = CommodityService;

    $scope.saveToServer = function() {
        return goods.create($scope.model);
    };

    $scope.goView = function() {
        return "index.good.view";
    };
})

.controller("GoodViewCntr", function($scope, $stateParams, $state, goods, config, item) {
   $scope.name_head = config.name;

   var id = $stateParams.id;
    $scope.model = item;

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
});