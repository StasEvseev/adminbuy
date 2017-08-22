/**
 * Created by user on 17.08.15.
 */

angular.module('collects.module', ['core.controllers']).constant('config', {
    name: "Инкассация",
    formname: "CollectForm"
})

.run(function($templateCache, $http) {
    $templateCache.put("CollectForm", $http.get("/static/newadmin/js/applications/collect/template/form.html"));
})


.config(function($stateProvider) {
    $stateProvider.state('index.collect', {
            data: {
                 roles: ['user']
            },
            abstract: true,
            url: '/collect'
        })
        .state('index.collect.list', {
            url: "?filter&page",
            views: {
                'content@index': {
                    templateUrl: "/static/newadmin/js/applications/collect/template/list.html",
                    controller: "CollectListCntr"
                }
            }
        })
        .state('index.collect.create', {
            url: '/create',
            views: {
                'content@index': {
                    templateUrl: "/static/newadmin/js/applications/collect/template/create.html",
                    controller: "CollectCreateCntr"
                }
            }
        })
        .state('index.collect.view', {
            url: "/:id",
            views: {
                'content@index': {
                    templateUrl: "/static/newadmin/js/applications/collect/template/view.html",
                    controller: "CollectViewCntr"
                }
            },
            resolve: {
                item: function(collects, $stateParams) {
                    return collects.getById(parseInt($stateParams.id))
                }
            }
        })
        .state('index.collect.view.edit', {
            url: "/edit",
            views: {
                'content@index': {
                    templateUrl: "/static/newadmin/js/applications/collect/template/edit.html",
                    controller: "CollectEditCntr"
                }
            }
        })
})

.controller("CollectListCntr", function($scope, $controller, config, collects) {
    $controller('BaseListController', {$scope: $scope});
    $scope.name_head = config.name;

    $scope.goCreate = function() {
        return "index.collect.create";
    };

    $scope.goView = function() {
        return "index.collect.view";
    };

    $scope.goList = function() {
        return "index.collect.list";
    };

    $scope.getService = function() {
        return collects;
    };
})

.controller("CollectCreateCntr", function($scope, $controller, collects, config, PointService, UserService) {
    $controller('BaseCreateController', {$scope: $scope});
    $scope.name_head = config.name;

    $scope.formname =  config.formname;
    $scope.PointService = PointService;
    $scope.UserService = UserService;

    $scope.datepickers = {
        dt: false
    };
    $scope.today = function() {
        $scope.model.date = new Date();
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
        'year-format': "'yy'",
        'starting-day': 1
    };

    $scope.saveToServer = function() {
        return collects.create($scope.model);
    };

    $scope.goView = function() {
        return "index.collect.view";
    };
})

.controller("CollectEditCntr", function($scope, $controller, collects, item, config, PointService, UserService) {
    $controller('BaseCreateController', {$scope: $scope});
    $scope.model = item;
    $scope.name_head = config.name;
    $scope.formname =  config.formname;
    $scope.PointService = PointService;
    $scope.UserService = UserService;

    $scope.datepickers = {
        dt: false
    };
    $scope.today = function() {
        $scope.model.date = new Date();
    };
//    $scope.today();
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
        'year-format': "'yy'",
        'starting-day': 1
    };

    $scope.saveToServer = function() {
        return collects.update($scope.model.id, $scope.model);
    };

    $scope.goView = function() {
        return "index.collect.view";
    };
})

.controller("CollectViewCntr", function($scope, $stateParams, $state, collects, config, item) {
    $scope.name_head = config.name;

    var id = $stateParams.id;
    $scope.model = item;
//    $scope.printBarCode = printBarCode;

    $scope.edit = function() {
        $state.go('index.collect.view.edit', {id: id});
    };

    $scope.delete_ = function() {
        if (confirm("Вы действительно хотите удалить запись?")) {
            deleteItem();
        }
    };

    function deleteItem() {
        collects.delete_(id).then(function(){
            $state.go("index.collect.list");
        });
    }

});