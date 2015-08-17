//'use strict';
AdminApp = angular.module('AdminApp', [
    'ui.router',
    'ui.select',
    'ui.bootstrap',

    'auth.ui',
    'auth.http',

    'core.service',
    'core.controllers',

    'mails.service',

    'invoices.module',
    'invoices.service',

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

var MailListController = function ($scope, $state, mailitems, mails, $stateParams) {

    hideSpinner();

    $scope.page = 1;
    $scope.countPerPage = 10;
    $scope.items = mailitems;
    $scope.checkMail = function () {
        console.log("CHECK MAIL");
    };

    if ($stateParams.filter) {
        $scope.searchText = $stateParams.filter;
    }
    if ($stateParams.page) {
        $scope.page = parseInt($stateParams.page);
    }

    $scope.boxTitle = $stateParams._new === "true" ? "Новые" : "Inbox";

    $scope.next = function () {
        if ($scope.hasNext()) {
            showSpinner();
            $state.go('index.mailbox.list', {filter: $scope.searchText, page: $scope.page + 1});
        }
    };

    $scope.prev = function () {
        if ($scope.hasPrev()) {
            showSpinner();
            $state.go('index.mailbox.list', {filter: $scope.searchText, page: $scope.page - 1});
        }
    };

    $scope.hasPrev = function () {
        return $scope.page > 1;
    };

    $scope.hasNext = function () {
        return $scope.page < mails.count() / $scope.countPerPage;
    };

    $scope.filter = function (text) {
        showSpinner();
        $state.go('index.mailbox.list', {filter: text, page: 1});
    };

    $scope.count = function () {
        return mails.count();
    };

    $scope.countNew = function () {
        return mails.countNew();
    };

    $scope.countNewM = function () {
        return mails.countNew();
    };

    function showSpinner() {
        $scope.loadingFinish = false;
    }

    function hideSpinner() {
        $scope.loadingFinish = true;
    }
};

AdminApp.controller("MailListController", MailListController);

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

//        .state('register', {
//            url: '/register',
//            views: {
//                'main@': {
//                    templateUrl: 'static/template/newadmin/registration.html',
//                    controller: function($scope, $state, principal) {
//                        $scope.register = function() {
//                            principal.registration({
//                                login: $scope.login,
//                                email: $scope.email,
//                                password: $scope.password,
//                                retypepassword: $scope.retypepassword
//                            }).then(
//                                function() {
//                                    $state.go('index.dash');
//                                },
//                                function(resp) {
//                                    debugger
//                                    $scope.is_error = true;
//
//                                });
//                        }
//                    }
//                }
//            }
//        })

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
        })

        .state('index.mailbox', {
            abstract: true,
            url: "/mailbox",
            views: {
                'content': {
                    templateUrl: "static/template/newadmin/mailbox/base.html"
                }
            }
        })

        .state('index.mailbox.list', {
            url: "?_new&filter&page",
            views: {
                'head': {
                    templateUrl: "static/template/newadmin/mailbox/list.head.html",
                    controller: "MailListController"
                },
                'item': {
                    templateUrl: "static/template/newadmin/mailbox/list.html",
                    controller: "MailListController"
                }
            },
            resolve: {
                mailitems: ['mails', '$stateParams',
                    function (mails, $stateParams) {
                        return mails.filter($stateParams.filter, $stateParams.page, $stateParams.count, $stateParams._new);
                    }]
            }
        })

        .state('index.mailbox.list.read', {
            url: "/{mailId:[0-9]{1,10}}",

            resolve: {
                item: function ($stateParams, mails) {
                    return mails.getById(parseInt($stateParams.mailId));
                }
            },
            views: {
                'head@index.mailbox': {
                    templateUrl: "static/template/newadmin/mailbox/read.head.html",
                    controller: function ($scope, item, mails) {
                        $scope.item = item;
                    }
                },
                '': {
                    templateUrl: "static/template/newadmin/mailbox/read.html",
                    controller: function ($scope, $stateParams, $state, item, mails) {
                        mails.setCurrent(item);
                        $scope.item = item;

                        $scope.hasNext = mails.hasNext;
                        $scope.hasPrev = mails.hasPrev;

                        $scope.prev = function() {
                            if (mails.hasPrev()) {
                                $scope.loadingFinish = false;
                                $state.go('index.mailbox.list.read', {mailId: mails.getPrev()});
                            }
                        };

                        $scope.next = function() {
                            if (mails.hasNext()) {
                                $scope.loadingFinish = false;
                                $state.go('index.mailbox.list.read', {mailId: mails.getNext()});
                            }
                        };
                    }
                }
            }

        });
});