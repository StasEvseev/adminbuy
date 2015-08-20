//'use strict';
AdminApp = angular.module('AdminApp', [
    'ui.router',
    'ui.select',
    'ui.bootstrap',

    'auth.ui',
    'auth.http',

    'core.service',
    'core.controllers',

    'mails.module',
    'mails.service',

    'invoices.module',
    'invoices.service',

    'provider.module',
    'provider.service',

    'commodity.module',
    'commodity.service',

    'good.module',
    'good.service',

    'pointsales.module',
    'pointsales.service',

    'receivers.module',
    'receivers.service',

    'users.module',
    'users.service',

    'user',
    'application',

    'filters',
    'directive',

    'ngTable',
    'angularSpinner',
    'ngSanitize'
]);

AdminApp.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
});

AdminApp.run(function($rootScope) {
    $rootScope.$on('$stateChangeSuccess', function(ev, to, toParams, from, fromParams) {
        $rootScope.previousState = from;
        $rootScope.previousStateParams = fromParams;
    });
});

AdminApp.run(function ($rootScope) {
    $rootScope._ = _;
});

var MainController = function ($scope, $rootScope, User, Company, Application, mails, $state, principal) {

    $scope.is_superuser = User.is_superuser();

    $scope.userName = User.name();
    $scope.position = User.position();
    $scope.companyName = Company.name();
    $scope.companyNameShort = Company.nameShort();
    $scope.version = Application.version();
    $scope.authorLink = Application.authorLink();

    var socket;
    socket = io.connect('http://' + document.domain + ':' + location.port); //, {resource: 'chat'});

    socket.on('connect', function () {
        socket.emit('connect', {data: 'I\'m connected!'});
    });

    socket.on('new mail', function (msg) {
        $rootScope.$apply(function () {
            mails.add(msg);
        });
    });

    socket.on("mail handle", function(resp) {
        $rootScope.$apply(function() {
            mails.remove(resp.id);
        });
    });

    $scope.logout = function () {
        principal.authenticate();
        $state.go("signin");
    };
};

AdminApp.controller("MainController", MainController);

AdminApp.controller('HeaderController', function ($scope, mails, User) {
    $scope.messages = function() {return mails.all_new()};
    $scope.iconUrl = User.iconUrl();

    $scope.countNew = function () {
        return mails.countNew();
    };
});

AdminApp.controller('SidebarController', function ($scope, mails, User) {
//    $scope.messages = function() {return mails.all_new()};
    $scope.iconUrl = User.iconUrl();

    $scope.countNew = function () {
        return mails.countNew();
    };
});

//Сервис загрузки данных
//Пример:
//Загрузка данных профиля пользователя до показа страницы.
AdminApp.service('LoadData', function($state, $rootScope, $q) {
    return {
        change: function() {
            var q = $q.defer();
            q.promise.then(function() {
                if ($rootScope.toState.name != 'index.load') {
                    $rootScope.toStateLoad = $rootScope.toState;
                    $rootScope.toStateLoadParams = $rootScope.toStateParams;
                    $state.go('index.load');
                }
            });

            q.resolve();

            return q.promise;
        }
    }
});

AdminApp.config(function ($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise("/");

    $stateProvider.state('site', {
        'abstract': true,
        resolve: {
            authorize: ['authorization', function (authorization) {
                return authorization.authorize();
            }],
            loadData: function(LoadData) {
                return LoadData.change();
            }
        }
    })

        .state('signin', {
            url: '/signin',
            views: {
                'main@': {
                    templateUrl: 'static/template/newadmin/login.html',
                    controller: function ($scope, $state, principal) {
                        $scope.signin = function () {

                            // here, we fake authenticating and give a fake user
                            principal.authenticate({
                                login: $scope.login,
                                password: $scope.password
                            }).then(
                                function () {
                                    if ($scope.returnToState) {
                                        $state.go($scope.returnToState.name, $scope.returnToStateParams);
                                    }
                                    else {
                                        $state.go('index.dash');
                                    }
                                },
                                function () {
                                    $scope.is_error = true;
                                });
                        };
                    }
                }
            }
        })

        .state('index.accessdenied', {
            views: {
                'content': {
                    templateUrl: "static/template/newadmin/403.html",
                    controller: function() {

                    }
                }
            }
        })

        .state('index', {
            parent: 'site',
            abstract: true,
            views: {
                'main@': {
                    templateUrl: "static/template/newadmin/admin.html",
                    controller: 'MainController'
                }
            }
        })

        .state('index.load', {
            views: {
                'main@': {
                    templateUrl: "static/template/newadmin/load.html",
                    controller: function($scope, $q, $rootScope, $state, $timeout, mails, User, Application, Company) {

                        $scope.max = 100;
                        $scope.type = 'info';

                        $scope.companyName = Company.name();

                        $scope.version = Application.version();
                        $scope.authorLink = Application.authorLink();

                        $scope.dynamic = 0;

                        $q.all([mails.fetch().then(function() {
                            $timeout(function() {
                                $scope.dynamic += 50;
                            }, 300);

                        }), User.fetch().then(function() {
                            $timeout(function() {
                                $scope.dynamic += 50;
                            }, 700);
                        })]).then(function() {
                            $timeout(function() {
                                $state.go($rootScope.toStateLoad.name, $rootScope.toStateLoadParams);
                            }, 1500);
                        });
                    }
                }
            }
        })

        .state('index.dash', {
            url: '/',
            views: {
                'content': {
                    templateUrl: 'static/template/newadmin/dash.html',
                    controller: function ($scope, $rootScope, Application) {
                        $scope.version = Application.version();
                    }
                }
            }
        });
});