/**
 * Created by user on 14.08.15.
 */

angular.module('provider.module', ['core.controllers']).constant('ProviderConfig', {
    name: "Поставщики",
    formname: "ProviderForm"
})

.run(function($templateCache, $http) {
    $templateCache.put("ProviderForm", $http.get("static/newadmin/js/applications/provider/template/form.html"));
})


.factory('ProviderService', function(BaseDictService, providers, $controller) {

    var child = Object.create(BaseDictService);
    child.records = function (text) {
        return providers.filter(text);
    };

    child.formInclude = function() {
        return "ProviderForm";
    };

    child.title = function() {
        return "Создание поставщика";
    };

    child.titleEdit = function() {
        return "Редактирование поставщика";
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
                return providers.getById(item.id);
            }
        };
    };

    return child;
})


.config(function($stateProvider) {
    $stateProvider.state('index.provider', {
            data: {
                 roles: ['user']
            },
            abstract: true,
            url: '/provider'
        })
        .state('index.provider.list', {
            url: "?filter&page",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/provider/template/list.html",
                    controller: "ProviderListCntr"
                }
            }
        })
        .state('index.provider.create', {
            url: '/create',
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/provider/template/create.html",
                    controller: "ProviderCreateCntr"
                }
            }
        })
        .state('index.provider.view', {
            url: "/:id",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/provider/template/view.html",
                    controller: "ProviderViewCntr"
                }
            },
            resolve: {
                item: function(providers, $stateParams) {
                    return providers.getById(parseInt($stateParams.id))
                }
            }
        })
        .state('index.provider.view.edit', {
            url: "/edit",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/provider/template/edit.html",
                    controller: "ProviderEditCntr"
                }
            }
        })
})

.controller("ProviderListCntr", function($scope, $controller, ProviderConfig, providers) {
    $controller('BaseListController', {$scope: $scope});
    $scope.name_head = ProviderConfig.name;

    $scope.goCreate = function() {
        return "index.provider.create";
    };

    $scope.goView = function() {
        return "index.provider.view";
    };

    $scope.goList = function() {
        return "index.provider.list";
    };

    $scope.getService = function() {
        return providers;
    };
})

.controller("ProviderCreateCntr", function($scope, $controller, providers, ProviderConfig) {
    $controller('BaseCreateController', {$scope: $scope});
    $scope.name_head = ProviderConfig.name;

    $scope.formname =  ProviderConfig.formname;

    $scope.saveToServer = function() {
        return providers.create($scope.model);
    };

    $scope.goView = function() {
        return "index.provider.view";
    };
})

.controller("ProviderEditCntr", function($scope, $controller, item, providers, ProviderConfig) {
    $controller('BaseCreateController', {$scope: $scope});
    $scope.model = item;
    $scope.name_head = ProviderConfig.name;
    $scope.formname =  ProviderConfig.formname;

    $scope.saveToServer = function() {
        return providers.create($scope.model);
    };

    $scope.goView = function() {
        return "index.provider.view";
    };
})

.controller("ProviderViewCntr", function($scope, $stateParams, $state, providers, ProviderConfig, item) {
   $scope.name_head = ProviderConfig.name;

   var id = $stateParams.id;
    $scope.model = item;

    $scope.edit = function() {
        $state.go('index.provider.view.edit', {id: id});
    };

    $scope.delete_ = function() {
        if (confirm("Вы действительно хотите удалить запись?")) {
            providers.delete_(id).then(function(){
                $state.go("index.provider.list");
            });
        }
    };
});