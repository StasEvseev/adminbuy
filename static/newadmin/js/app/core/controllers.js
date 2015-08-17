/**
 * Created by user on 29.07.15.
 */

angular.module("core.controllers", ['ui.router', 'form', 'ngTable'])
.controller("BaseCreateController", function($scope, $rootScope, $state, Form, $timeout, $q) {

    $scope.loadingFinish = true;
    $scope.model = {};

    $scope.Form = Form;

    $scope.cancel = function () {
        if($state.$current.parent && !$state.$current.parent.self.abstract) {
            $state.go($state.$current.parent.self.name, $state.toStateParams);
        }
        else if(!$rootScope.previousState.abstract && $rootScope.previousState.name != 'index.load') {
            $state.go($rootScope.previousState, $rootScope.previousStateParams);
        } else {
            $state.go($scope.goList());
        }
    };

    $scope.save = function() {
        if($scope.validate()) {
            $scope.loadingFinish = false;
            $scope.saveToServer().then(function(resp) {
                Form.updateView();
                $scope.loadingFinish = true;
                $state.go($scope.goView(), {id: resp.data.id});
            }, function(resp) {
                $scope.loadingFinish = true;
            });
        } else {
            Form.setSubmitted();
        }
    };

    $scope.saveToServer = function() {
        var q = $q.defer();
        $timeout(function(){
            q.resolve();
        }, 3000);
        return q.promise;
    };

    $scope.validate = function() {
        return Form.isValid();
    };

    $scope.myForm = {};

    Form.setCurrentForm($scope.myForm);

    $scope.goList = function() {
        return "";
    };

    $scope.goView = function() {
        return "";
    };
})

.controller("BaseListController", function($scope, $stateParams, $state, ngTableParams) {
    $scope.page = 1;
    $scope.countPerPage = 10;

    if ($stateParams.filter) {
        $scope.searchText = $stateParams.filter;
    }
    if ($stateParams.page) {
        $scope.page = parseInt($stateParams.page);
    }
    $scope.loadingFinish = true;

    $scope.goList = function() {
        return "";
    };

    $scope.goCreate = function() {
        return "";
    };

    $scope.goView = function() {
        return "";
    };

    $scope.getService = function() {
        return undefined;
    };

    $scope.tableParams = new ngTableParams({
            page: $scope.page,            // show first page
            count: 10,          // count per page
            sorting: {
                name: 'asc'     // initial sorting
            }
        },
        {
            total: 0, // length of data
            counts: [], // hide page counts control
            getData: function ($defer, params) {
                // use build-in angular filter
                var orig_page_func = params.page;
                params.page = function (arg) {
                    if (angular.isDefined(arg)) {
                        $state.go($scope.goList(), {filter: $scope.searchText, page: arg})
                    } else {
                        return orig_page_func();
                    }
                };

                $scope.loadingFinish = false;

                $scope.getService().filter($scope.searchText, $scope.page, params.count()).then(
                    function (data) {
                        $defer.resolve(data);
                        params.total($scope.getService().count());
                        $scope.loadingFinish = true;
                    });
            }
        });

    $scope.detail = function (id) {
        $scope.loadingFinish = false;
        $state.go($scope.goView(), {id: id}).then(function () {
            $scope.loadingFinish = true;
        });
    };

    $scope.filter = function (text) {
        $state.go($scope.goList(), {filter: text, page: 1});
    };

    $scope.create = function () {
        $state.go($scope.goCreate());
    };
});