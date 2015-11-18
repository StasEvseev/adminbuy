/**
 * Created by user on 30.07.15.
 */

angular.module('pointsales.module', ['ui.router', 'ui.bootstrap', 'core.service', 'core.controllers', 'pointsales.service', 'form'])

.run(function($templateCache, $http) {
    $templateCache.put("PointsaleForm", $http.get("static/newadmin/js/applications/pointsale/template/form.html"));
})

.factory('PointService', function(BaseDictService, pointsales, $controller) {

    var child = Object.create(BaseDictService);
    child.records = function (text) {
        return pointsales.filter(text);
    };

    child.formInclude = function() {
        return "PointsaleForm";
    };

    child.title = function() {
        return "Создание торговой точки";
    };

    child.titleEdit = function() {
        return "Редактирование торговой точки";
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
                return pointsales.getById(item.id);
            }
        };
    };

    return child;
})

.config(function($stateProvider) {
    $stateProvider.state('index.pointsale', {
            data: {
                 roles: ['user']
            },
            abstract: true,
            url: '/pointsale'
        })
        .state('index.pointsale.list', {
            url: "?filter&page",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/pointsale/template/list.html",
                    controller: "PointsaleListCntr"
                }
            }
        })
        .state('index.pointsale.create', {
            url: '/create',
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/pointsale/template/create.html",
                    controller: "PointsaleCreateCntr"
                }
            }
        })
        .state('index.pointsale.view', {
            url: "/:id",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/pointsale/template/view.html",
                    controller: "PointsaleViewCntr"
                }
            },
            resolve: {
                item: function(pointsales, $stateParams) {
                    return pointsales.getById(parseInt($stateParams.id))
                }
            }
        })
        .state('index.pointsale.view.edit', {
            url: "/edit",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/pointsale/template/edit.html",
                    controller: "PointsaleEditCntr"
                }
            }
        })
})
.controller('PointsaleListCntr', function($scope, $controller, pointsales) {
    $controller('BaseListController', {$scope: $scope});

    $scope.goList = function() {
        return 'index.pointsale.list';
    };

    $scope.goView = function() {
        return 'index.pointsale.view';
    };

    $scope.goCreate = function() {
        return "index.pointsale.create";
    };

    $scope.getService = function() {
        return pointsales;
    };
})
.controller('PointsaleViewCntr', function($scope, $rootScope, $controller, $stateParams, $state, item, pointsales, pointsalesgoods) {

    var id = $stateParams.id;
    $scope.model = item;

    var $scopeGood = $rootScope.$new();

    $controller('GoodListCntr', {$scope: $scopeGood});

    $scopeGood.getService = function() {
        var serv  = pointsalesgoods;
        serv.setPointId(id);
        return serv;
    };

    $scope.$scopeGood = $scopeGood;

    $scope.edit = function() {
        $state.go('index.pointsale.view.edit', {id: id});
    };

    $scope.delete_ = function() {
        if (confirm("Вы действительно хотите удалить запись?")) {
            pointsales.delete_(id).then(function(){
                $state.go("index.pointsale.list");
            });
        }
    };
})
.controller("PointsaleCreateCntr", function($scope, $controller, pointsales) {
    $controller('BaseCreateController', {$scope: $scope});

    $scope.goList = function() {
        return "index.pointsale.list";
    };

    $scope.goView = function() {
        return "index.pointsale.view";
    };

    $scope.saveToServer = function() {
        return pointsales.create($scope.model);
    };
})

.controller("PointsaleEditCntr", function($scope, $controller, $stateParams, item, pointsales) {
    $controller('BaseCreateController', {$scope: $scope});
    $scope.model = item;

    $scope.saveToServer = function() {
        return pointsales.update(parseInt($stateParams.id), $scope.model);
    };

    $scope.goList = function() {
        return "index.pointsale.list";
    };

    $scope.goView = function() {
        return "index.pointsale.view";
    };
});