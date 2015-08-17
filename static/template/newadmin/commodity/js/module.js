/**
 * Created by user on 14.08.15.
 */

angular.module('commodity.module', ['core.controllers']).constant('config', {
    name: "Номенклатура",
    formname: "CommodityForm"
})

.run(function($templateCache, $http) {
    $templateCache.put("CommodityForm", $http.get("static/template/newadmin/commodity/form.html"));
})


.config(function($stateProvider) {
    $stateProvider.state('index.commodity', {
            abstract: true,
            url: '/commodity'
        })
        .state('index.commodity.list', {
            url: "?filter&page",
            views: {
                'content@index': {
                    templateUrl: "static/template/newadmin/commodity/list.html",
                    controller: "CommodityListCntr"
                }
            }
        })
        .state('index.commodity.create', {
            url: '/create',
            views: {
                'content@index': {
                    templateUrl: "static/template/newadmin/commodity/create.html",
                    controller: "CommodityCreateCntr"
                }
            }
        })
        .state('index.commodity.view', {
            url: "/:id",
            views: {
                'content@index': {
                    templateUrl: "static/template/newadmin/commodity/view.html",
                    controller: "CommodityViewCntr"
                }
            },
            resolve: {
                item: function(commodities, $stateParams) {
                    return commodities.getById(parseInt($stateParams.id))
                }
            }
        })
        .state('index.commodity.view.edit', {
            url: "/edit",
            views: {
                'content@index': {
                    templateUrl: "static/template/newadmin/commodity/edit.html",
                    controller: "CommodityEditCntr"
                }
            }
        })
})

.controller("CommodityListCntr", function($scope, $controller, config, commodities) {
    $controller('BaseListController', {$scope: $scope});
    $scope.name_head = config.name;

    $scope.goCreate = function() {
        return "index.commodity.create";
    };

    $scope.goView = function() {
        return "index.commodity.view";
    };

    $scope.goList = function() {
        return "index.commodity.list";
    };

    $scope.getService = function() {
        return commodities;
    };
})

.controller("CommodityCreateCntr", function($scope, $controller, config) {
    $controller('BaseCreateController', {$scope: $scope});
    $scope.name_head = config.name;

    $scope.formname =  config.formname;
})

.controller("CommodityEditCntr", function($scope, $controller, item, config) {
    $controller('BaseCreateController', {$scope: $scope});
    $scope.model = item;
    $scope.name_head = config.name;
    $scope.formname =  config.formname;
})

.controller("CommodityViewCntr", function($scope, $stateParams, $state, commodities, config, item) {
   $scope.name_head = config.name;

   var id = $stateParams.id;
    $scope.model = item;

    $scope.edit = function() {
        $state.go('index.commodity.view.edit', {id: id});
    };

    $scope.delete_ = function() {
        if (confirm("Вы действительно хотите удалить запись?")) {
            commodities.delete_(id).then(function(){
                $state.go("index.commodity.list");
            });
        }
    };
});