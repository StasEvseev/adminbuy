/**
 * Created by user on 29.07.15.
 */

angular.module("receivers.module", ['ui.router', 'core.service', 'core.controllers', 'receivers.service', 'form'])
.run(function($templateCache, $http) {
    $templateCache.put("ReceiverForm", $http.get("static/template/newadmin/receiver/form.html"));
})

.factory('ReceiverService', function(BaseDictService, receivers) {

    var child = Object.create(BaseDictService);
    child.records = function (text) {
        return receivers.filter(text);
    };

    child.formInclude = function() {
        return "ReceiverForm";
    };

    child.title = function() {
        return "Создание оптовика";
    };

    child.titleEdit = function() {
        return "Редактирование оптовика";
    };

//    child.controller = function() {
//        return function($scope, $modalInstance) {
//            var parent = BaseDictService.controller();
//            $controller(parent, {$scope: $scope, $modalInstance: $modalInstance});
//        }
//    };

    child.resolveEdit = function(item) {
        return {
            item: function() {
                return receivers.getById(item.id);
            }
        };
    };

    return child;
})

.config(function($stateProvider) {
    $stateProvider.state('index.receiver', {
            abstract: true,
            url: '/receiver'
        })
        .state('index.receiver.list', {
            url: "?filter&page",
            views: {
                'content@index': {
                    templateUrl: "static/template/newadmin/receiver/list.html",
                    controller: "ReceiverListCntr"
                }
            }
        })
        .state('index.receiver.create', {
            url: '/create',
            views: {
                'content@index': {
                    templateUrl: "static/template/newadmin/receiver/create.html",
                    controller: "ReceiverCreateCntr"
                }
            }
        })
        .state('index.receiver.view', {
            url: "/:id",
            views: {
                'content@index': {
                    templateUrl: "static/template/newadmin/receiver/view.html",
                    controller: "ReceiverViewCntr"
                }
            },
            resolve: {
                item: function(receivers, $stateParams) {
                    return receivers.getById(parseInt($stateParams.id))
                }
            }
        })
        .state('index.receiver.view.edit', {
            url: "/edit",
            views: {
                'content@index': {
                    templateUrl: "static/template/newadmin/receiver/edit.html",
                    controller: "ReceiverEditCntr"
                }
            }
        })
});

AdminApp.controller('ReceiverListCntr', function($scope, receivers, $controller) {
    $controller('BaseListController', {$scope: $scope});

    $scope.goList = function() {
        return 'index.receiver.list';
    };

    $scope.goCreate = function() {
        return "index.receiver.create";
    };

    $scope.goView = function() {
        return 'index.receiver.view';
    };

    $scope.getService = function() {
        return receivers;
    };
})

.controller('ReceiverViewCntr', function($scope, $stateParams, $state, item, receivers) {
        var id = $stateParams.id;
    $scope.model = item;

    $scope.edit = function() {
        $state.go('index.receiver.view.edit', {id: id});
    };

    $scope.delete_ = function() {
        if (confirm("Вы действительно хотите удалить запись?")) {
            receivers.delete_(id).then(function(){
                $state.go("index.receiver.list");
            });
        }
    };
})

.controller("ReceiverCreateCntr", function($scope, $controller, receivers) {
    $controller('BaseCreateController', {$scope: $scope});

    $scope.goList = function() {
        return "index.receiver.list";
    };

    $scope.goView = function() {
        return "index.receiver.view";
    };

    $scope.saveToServer = function() {
        return receivers.create($scope.model);
    };
})
.controller("ReceiverEditCntr", function($scope, $controller, $stateParams, item, receivers) {
    $controller('BaseCreateController', {$scope: $scope});

    $scope.model = item;

    $scope.saveToServer = function() {
        return receivers.update(parseInt($stateParams.id), $scope.model);
    };

    $scope.goList = function() {
        return "index.receiver.list";
    };

    $scope.goView = function() {
        return "index.receiver.view";
    };
});