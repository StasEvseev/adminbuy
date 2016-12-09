/**
 * Created by user on 12.08.15.
 */

/**
 * Created by user on 29.07.15.
 */

angular.module("users.module", ['ui.router', 'core.service', 'core.controllers', 'users.service', 'form'])
.run(function($templateCache, $http) {
    $templateCache.put("UserForm", $http.get("/static/newadmin/js/applications/user/template/form.html"));
})

.factory('UserService', function(BaseDictService, users, $controller) {

    var child = Object.create(BaseDictService);
    child.records = function (text) {
        return users.filter(text);
    };

    child.formInclude = function() {
        return "UserForm";
    };

    child.title = function() {
        return "Создание пользователя";
    };

    child.titleEdit = function() {
        return "Редактирование пользователя";
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
                return users.getById(item.id);
            }
        };
    };

    return child;
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
                    templateUrl: "/static/newadmin/js/applications/user/template/list.html",
                    controller: "UserListCntr"
                }
            }
        })
        .state('index.user.create', {
            url: '/create',
            views: {
                'content@index': {
                    templateUrl: "/static/newadmin/js/applications/user/template/create.html",
                    controller: "UserCreateCntr"
                }
            }
        })
        .state('index.user.view', {
            url: "/:id",
            views: {
                'content@index': {
                    templateUrl: "/static/newadmin/js/applications/user/template/view.html",
                    controller: "UserViewCntr"
                }
            },
            resolve: {
                item: function(users, $stateParams) {
                    return users.getById(parseInt($stateParams.id))
                },
                profile: function($http, $stateParams, $q) {
                    var q = $q.defer();
                    var name, iconUrl, position, is_superuser, id;
                    $http.get('/api/profile_by_id/' + $stateParams.id).then(function(resp) {
                        name = resp.data.name;
                        iconUrl = resp.data.iconUrl;
                        position = resp.data.position;
                        is_superuser = resp.data.is_superuser;
                        id = resp.data.id;

                        q.resolve({
                            name: name,
                            iconUrl: iconUrl,
                            position: position,
                            is_superuser: is_superuser,
                            id: id
                        })
                    }, function(resp) {
                        id: '';
                        name = '';
                        iconUrl = '';
                        position = '';
                        is_superuser = '';
                        q.resolve({
                            name: name,
                            iconUrl: iconUrl,
                            position: position,
                            is_superuser: is_superuser,
                            id: id
                        })
                    });





                    return q.promise;

                    //return
                }
            }
        })
        .state('index.user.view.edit', {
            url: "/edit",
            views: {
                'content@index': {
                    templateUrl: "/static/newadmin/js/applications/user/template/edit.html",
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

.controller('UserViewCntr', function($scope, $stateParams, $state, item, users, profile) {
        var id = $stateParams.id;
    $scope.model = item;

    $scope.iconUrl = profile.iconUrl;

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

.controller("UserCreateCntr", function($scope, $controller, users, RoleService) {
    $controller('BaseCreateController', {$scope: $scope});

    $scope.RoleService = RoleService;

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
.controller("UserEditCntr", function($scope, $controller, $stateParams, RoleService, item, users) {
    $controller('BaseCreateController', {$scope: $scope});

    $scope.RoleService = RoleService;

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
