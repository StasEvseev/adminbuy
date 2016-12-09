/**
 * Created by user on 14.08.15.
 */

angular.module('commodity.module', ['core.controllers']).constant('CommodityConfig', {
    name: "Номенклатура",
    formname: "CommodityForm"
})

.run(function($templateCache, $http) {
    $templateCache.put("CommodityForm", $http.get("/static/newadmin/js/applications/commodity/template/form.html"));
})


.factory('CommodityService', function(BaseDictService, commodities, $controller) {

    var child = Object.create(BaseDictService);
    child.records = function (text) {
        return commodities.filter(text);
    };

    child.formInclude = function() {
        return "CommodityForm";
    };

    child.title = function() {
        return "Создание номенклатуры";
    };

    child.titleEdit = function() {
        return "Редактирование номенклатуры";
    };

    child.controller = function() {
        return function($scope, $modalInstance) {
            var parent = BaseDictService.controller();
            $controller(parent, {$scope: $scope, $modalInstance: $modalInstance});
        }
    };

    child.resolveEdit = function(item) {
        return {
            item: function() {
                return commodities.getById(item.id);
            }
        };
    };

    return child;
})


.config(function($stateProvider) {
    $stateProvider.state('index.commodity', {
            data: {
                 roles: ['user']
            },
            abstract: true,
            url: '/commodity'
        })
        .state('index.commodity.list', {
            url: "?filter&page",
            views: {
                'content@index': {
                    templateUrl: "/static/newadmin/js/applications/commodity/template/list.html",
                    controller: "CommodityListCntr"
                }
            }
        })
        .state('index.commodity.create', {
            url: '/create',
            views: {
                'content@index': {
                    templateUrl: "/static/newadmin/js/applications/commodity/template/create.html",
                    controller: "CommodityCreateCntr"
                }
            }
        })
        .state('index.commodity.view', {
            url: "/:id",
            views: {
                'content@index': {
                    templateUrl: "/static/newadmin/js/applications/commodity/template/view.html",
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
                    templateUrl: "/static/newadmin/js/applications/commodity/template/edit.html",
                    controller: "CommodityEditCntr"
                }
            }
        })
})

.controller("CommodityListCntr", function($scope, $controller, CommodityConfig, commodities) {
    $controller('BaseListController', {$scope: $scope});
    $scope.name_head = CommodityConfig.name;

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

.controller("CommodityCreateCntr", function($scope, $controller, commodities, CommodityConfig) {
    $controller('BaseCreateController', {$scope: $scope});
    $scope.name_head = CommodityConfig.name;

    $scope.formname =  CommodityConfig.formname;

    $scope.saveToServer = function() {
        return commodities.create($scope.model);
    };

    $scope.goView = function() {
        return "index.commodity.view";
    };
})

.controller("CommodityEditCntr", function($scope, $controller, item, commodities, CommodityConfig) {
    $controller('BaseCreateController', {$scope: $scope});
    $scope.model = item;
    $scope.name_head = CommodityConfig.name;
    $scope.formname =  CommodityConfig.formname;

    $scope.saveToServer = function() {
        return commodities.create($scope.model);
    };

    $scope.goView = function() {
        return "index.commodity.view";
    };
})

.controller("CommodityViewCntr", function($scope, $stateParams, $state, commodities, CommodityConfig, item) {
   $scope.name_head = CommodityConfig.name;

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
