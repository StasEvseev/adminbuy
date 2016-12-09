
angular.module('{{ name }}.module', ['core.controllers', '{{ name }}.service']).constant('{{ name_cap }}Config', {
    name: "Скаффолд",
    formname: "{{ name_cap }}Form"
})

.run(function($templateCache, $http) {
    $templateCache.put("{{ name_cap }}Form", $http.get("static/newadmin/js/applications/{{ name }}/template/form.html"));
})


.config(function($stateProvider) {
    $stateProvider.state('index.{{ name }}', {
            data: {
                 roles: ['user']
            },
            abstract: true,
            url: '/{{ name }}'
        })
        .state('index.{{ name }}.list', {
            url: "?filter&page",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/{{ name }}/template/list.html",
                    controller: "{{ name_cap }}ListCntr"
                }
            }
        })
        .state('index.{{ name }}.create', {
            url: '/create',
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/{{ name }}/template/create.html",
                    controller: "{{ name_cap }}CreateCntr"
                }
            }

        })
        .state('index.{{ name }}.view', {
            url: "/:id",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/{{ name }}/template/view.html",
                    controller: "{{ name_cap }}ViewCntr"
                }
            },
            resolve: {
                item: function({{ name_service }}, $stateParams) {
                    return {{ name_service }}.getById(parseInt($stateParams.id))
                }
            }
        })
        .state('index.{{ name }}.view.edit', {
            url: "/edit",
            views: {
                'content@index': {
                    templateUrl: "static/newadmin/js/applications/{{ name }}/template/edit.html",
                    controller: "{{ name_cap }}EditCntr"
                }
            },
            resolve: {

            }
        })
})

.controller("{{ name_cap }}ListCntr", function($scope, $controller, {{ name_cap }}Config, {{ name_service }}) {
    $controller('BaseListController', {$scope: $scope});
    $scope.name_head = {{ name_cap }}Config.name;

    $scope.goCreate = function() {
        return "index.{{ name }}.create";
    };

    $scope.goView = function() {
        return "index.{{ name }}.view";
    };

    $scope.goList = function() {
        return "index.{{ name }}.list";
    };

    $scope.getService = function() {
        return {{ name_service }};
    };
})

.controller("{{ name_cap }}CreateCntr", function($scope, $controller, {{ name_service }}, {{ name_cap }}Config) {
    $controller('BaseCreateController', {$scope: $scope});
    $scope.name_head = {{ name_cap }}Config.name;

    $scope.formname =  {{ name_cap }}Config.formname;

    $scope.saveToServer = function() {
        return {{ name_service }}.create($scope.model);
    };

    $scope.goView = function() {
        return "index.{{ name }}.view";
    };

    $scope.goList = function() {
        return "index.{{ name }}.list";
    };
})

.controller("{{ name_cap }}EditCntr", function($scope, $controller, $state, {{ name_service }}, {{ name_cap }}Config) {
    $controller('BaseCreateController', {$scope: $scope});

    $scope.name_head = {{ name_cap }}Config.name;
    $scope.formname =  {{ name_cap }}Config.formname;

    $scope.goView = function() {
        return "index.{{ name }}.view";
    };

    $scope.model = item;

    $scope.loadingFinish = true;

    //$scope._goCancel = function() {
    //    $state.go("index.{{ name }}.view", {mailId: $scope.item.id});
    //};

    $scope.save = function() {
        $scope.loadingFinish = false;

    };
})

.controller("{{ name_cap }}ViewCntr", function($scope, $stateParams, $state, item, {{ name_cap }}Config) {
    $scope.name_head = {{ name_cap }}Config.name;

    $scope.loadingFinish = true;

    var id = $stateParams.id;
    $scope.model = item;

    $scope.edit = function() {
        $scope.loadingFinish = false;
        $state.go('index.{{ name }}.view.edit', {id: id}).then(function() {
            $scope.loadingFinish = true;
        });

    };

    $scope.delete_ = function() {
        if (confirm("Вы действительно хотите удалить запись?")) {
            {{ name_service }}.delete_(id).then(function(){
                $state.go("index.{{ name }}.list");
            });
        }
    };
});
