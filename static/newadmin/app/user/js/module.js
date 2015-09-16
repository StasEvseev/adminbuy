/**
 * Created by user on 12.08.15.
 */

/**
 * Created by user on 29.07.15.
 */

angular.module("users.module", ['ui.router', 'core.service', 'core.controllers', 'users.service', 'form'])
.run(function($templateCache, $http) {
    $templateCache.put("UserForm", $http.get("static/newadmin/app/user/template/form.html"));
})

.config(function($stateProvider) {
    $stateProvider.state('index.user', {
            abstract: true,
            url: '/user',
        data: {
            roles: ['admin']
        }
        })
        .state('index.user.list', {
            url: "?filter&page",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/app/user/template/list.html",
                    controller: "UserListCntr"
                }
            }
        })
        .state('index.user.create', {
            url: '/create',
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/app/user/template/create.html",
                    controller: "UserCreateCntr"
                }
            }
        })
        .state('index.user.view', {
            url: "/:id",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/app/user/template/view.html",
                    controller: "UserViewCntr"
                }
            },
            resolve: {
                item: function(users, $stateParams) {
                    return users.getById(parseInt($stateParams.id))
                }
            }
        })
        .state('index.user.view.edit', {
            url: "/edit",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/app/user/template/edit.html",
                    controller: "UserEditCntr"
                }
            }
        })
});

AdminApp.controller('UserListCntr', function($scope, users, $controller) {
    $controller('BaseListController', {$scope: $scope});

    $scope.goList = function() {
        return 'index.user.list';
    };

    $scope.goCreate = function() {
        return "index.user.create";
    };

    $scope.goView = function() {
        return 'index.user.view';
    };

    $scope.getService = function() {
        return users;
    };
})

.controller('UserViewCntr', function($scope, $stateParams, $state, item, users) {
        var id = $stateParams.id;
    $scope.model = item;

    $scope.edit = function() {
        $state.go('index.user.view.edit', {id: id});
    };

    $scope.delete_ = function() {
        if (confirm("Вы действительно хотите удалить запись?")) {
            users.delete_(id).then(function(){
                $state.go("index.user.list");
            });
        }
    };
})

.controller("UserCreateCntr", function($scope, $controller, users) {
    $controller('BaseCreateController', {$scope: $scope});

    $scope.goList = function() {
        return "index.user.list";
    };

    $scope.goView = function() {
        return "index.user.view";
    };

    $scope.saveToServer = function() {
        return users.create($scope.model);
    };
})
.controller("UserEditCntr", function($scope, $controller, $stateParams, item, users) {
    $controller('BaseCreateController', {$scope: $scope});

    $scope.model = item;

    $scope.saveToServer = function() {
        return users.update(parseInt($stateParams.id), $scope.model);
    };

    $scope.goList = function() {
        return "index.user.list";
    };

    $scope.goView = function() {
        return "index.user.view";
    };
});