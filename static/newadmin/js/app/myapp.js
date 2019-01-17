//'use strict';
AdminApp = angular.module('AdminApp', [
    'ui.router',
    'ui.select',
    'ui.bootstrap',

    'qtip2',

    'auth.ui',
    'auth.http',

    'core.service',
    'core.controllers',

    'mails.module',
    'mails.service',

    'invoice.service',
    'invoice.module',

    'waybill.module',
    'waybill.service',

    'provider.module',
    'provider.service',

    'commodity.module',
    'commodity.service',

    'good.module',
    'good.service',

    'collects.module',
    'collects.service',

    'acceptance.module',
    'acceptance.service',

    'pointsales.module',
    'pointsales.service',

    'receivers.module',
    'receivers.service',

    'users.module',
    'users.service',

    'session.module',
    'session.service',

    'user',
    'application',

    'utils',

    'filters',
    'directive',

    'ngTable',
    'angularSpinner',
    'ngSanitize',
    'ds.clock',
    'luegg.directives',


    'anguFixedHeaderTable',

    'Firestitch.angular-counter',
    'dbApp'
]);

AdminApp.factory('Device', function($window) {
    return {
        getIfDefined: function() {
            if (angular.isUndefined($window.localStorage.deviceId)) {
                this.gen();
            }
            return this.getId();
        },
        getId: function() {
            return $window.localStorage.deviceId;
        },
        gen: function() {
            $window.localStorage.deviceId = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
                return v.toString(16);
            });
        }
    }
});

AdminApp.factory('hIDScanner', function($rootScope, $window, $timeout) {
    var sub = false;
        return {
            initialize : function() {
                var chars = [];
                var pressed = false;
                sub = true;
                angular.element($window).on('keypress', function(e) {
                    if (e.which >= 48 && e.which <= 57) {
                        chars.push(String.fromCharCode(e.which));
                    }
                    // console.log(e.which + ":" + chars.join("|"));
                    if (pressed == false) {
                        $timeout(function(){
                            if (chars.length >= 10) {
                                var barcode = chars.join("");
                                $rootScope.$broadcast("hidScanner::scanned", {barcode: barcode});
                            }
                            chars = [];
                            pressed = false;
                        },250);
                    }
                    pressed = true;
                });
            },
            uninitialize: function() {
                if (sub) {
                    angular.element($window).unbind("keypress");
                }
            }
        };
    });

AdminApp.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
});

AdminApp.constant('apiConfig', {
  baseUrl: '{{ api_location }}',
});

AdminApp.run(function($rootScope) {
    $rootScope.$on('$stateChangeSuccess', function(ev, to, toParams, from, fromParams) {
        $rootScope.previousState = from;
        $rootScope.previousStateParams = fromParams;
    });
});

AdminApp.run(function ($rootScope, $timeout, $window) {
    $rootScope._ = _;

    $($window).on("message", function(e){
        console.log(e);
    });

    $timeout(function() {
        console.log("BLA!");
    }, 1000);

});

var MainController = function ($scope, $rootScope, User, Company, Application, mails, $state, principal) {

    $scope.is_superuser = User.is_superuser();

    $scope.userName = User.name();
    $scope.position = User.position();
    $scope.companyName = Company.name();
    $scope.companyNameShort = Company.nameShort();
    $scope.version = Application.version();
    $scope.authorLink = Application.authorLink();

    $scope.aboutMe = aboutMe;
    $scope.logout = logout;

    var socket;
    socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port); //, {resource: 'chat'});

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

    function logout() {
        console.info("Unauthenticate.");
        principal.authenticate();
        $state.go("signin");
    }

    function aboutMe() {
        console.info("aboutMe");
        $state.go("index.user.view", {id: User.id()});
    }
};

AdminApp.factory("ShowHideRoles", function($state, principal) {
    return {
        showState: function(path) {
            var state = $state.get(path);
            var roles = state.data.roles || [];
            return principal.permissionRoles(roles);
        },
        showRole: function(roles) {
            return principal.permissionRoles(roles);
        }
    }
});

AdminApp.controller("MainController", MainController);

AdminApp.controller('HeaderController', function ($scope, $rootScope, mails, User, ShowHideRoles) {
    /*
    * Контроллер верхней панели.
    * */
    $scope.messages = function() {return mails.all_new()};
    $scope.iconUrl = User.iconUrl();

    $scope.countNew = function () {
        return mails.countNew();
    };

    $scope.toggle = handlerToggleBtn;

    $scope.show = ShowHideRoles.showState;

    function handlerToggleBtn(event) {
        event.preventDefault();
        $rootScope.$broadcast("toggleSidebar");
    }
});

AdminApp.controller('SidebarController', function ($scope, $rootScope, ShowHideRoles, mails, User) {
    /*
    * Контроллер боковой панели.
    * */
    $scope.iconUrl = User.iconUrl();

    var status = $("#status-line > span");
    var icon = $("#status-line > i");

    $scope.countNew = function () {
        return mails.countNew();
    };

    $rootScope.$on("toggleSidebar", function(arg, value) {
        console.info("Event toggleSidebar");
        toggleSidebar(value ? value.value : undefined);
    });

    $rootScope.$on('online', function(arg, status) {
       if(status.status == true) {
           $scope.onLine();
       } else {
           $scope.offLine();
       }
    });

    $scope.onLine = function() {
        icon.removeClass("text-warning");
        icon.addClass("text-success");
        status.text("Online");
    };

    $scope.offLine = function() {
        icon.removeClass("text-success");
        icon.addClass("text-warning");
        status.text("Offline");
    };

    $scope.show = ShowHideRoles.showState;

    //TODO магия
    var stateSidebar = {
        toggle: window.innerWidth < 768
    };

    function toggleSidebar(value) {

        if (value != undefined) {
            if (value != stateSidebar.toggle) {
                changeTog();
                stateSidebar.toggle = value;
            }
        } else {
            changeTog();
            stateSidebar.toggle = !stateSidebar.toggle;
        }

        function changeTog() {
            var screenSizes = $.AdminLTE.options.screenSizes;

            //Enable sidebar push menu
            if ($(window).width() > (screenSizes.sm - 1)) {
              $("body").toggleClass('sidebar-collapse');
            }
            //Handle sidebar push menu for small screens
            else {
              if ($("body").hasClass('sidebar-open')) {
                $("body").removeClass('sidebar-open');
                $("body").removeClass('sidebar-collapse')
              } else {
                $("body").addClass('sidebar-open');
              }
            }
        }
    }
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
                    templateUrl: '/static/newadmin/template/login.html',
                    controller: function ($scope, $rootScope, $state, principal) {
                        $scope.loadingFinish = true;
                        $scope.signin = function () {

                            var btn_sub = $("button[type='submit']");
                            btn_sub.prop('disabled', true);

                            $scope.loadingFinish = false;

                            principal.authenticate({
                                login: $scope.login,
                                password: $scope.password
                            }).then(successAuthenticate, failureAuthenticate);

                            function successAuthenticate() {
                                btn_sub.prop('disabled', false);
                                $scope.loadingFinish = true;
                                $scope.is_error = false;
                                if ($scope.returnToState) {
                                    $state.go($scope.returnToState.name, $scope.returnToStateParams);
                                }
                                else {
                                    //Если права выданы только как на продавца - то делаем переход на выбор рабочего дня
                                    var id = principal.getIdentity();
                                    if (id.length == 1 && id.indexOf("vendor") != -1) {
                                        console.info("You are only vendor. Go to vendor's menu.");
                                        $state.go('index.session.menu');
                                    } else {
                                        console.info("Don't you are not only vendor. Go to dash.");
                                        $state.go('index.dash');
                                    }
                                }
                            }

                            function failureAuthenticate(message) {
                                $scope.error = message;
                                btn_sub.prop('disabled', false);
                                $scope.loadingFinish = true;
                                $scope.is_error = true;
                            }
                        };
                    }
                }
            }
        })

        .state('index.accessdenied', {
            url: '/403',
            views: {
                'content': {
                    templateUrl: "/static/newadmin/template/403.html",
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
                    templateUrl: "/static/newadmin/template/admin.html",
                    controller: 'MainController'
                }
            }
        })

        .state('index.load', {
            views: {
                'main@': {
                    templateUrl: "/static/newadmin/template/load.html",
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

                        }, function(isOnline) {
                            $timeout(function() {
                                $scope.dynamic += 50;
                            }, 300);
                        }), User.fetch().then(function() {
                            $timeout(function() {
                                $scope.dynamic += 50;
                            }, 700);
                        }, function() {
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
                    templateUrl: '/static/newadmin/template/dash.html',
                    controller: function ($scope, $rootScope, Application, ShowHideRoles, mails) {
                        $scope.version = Application.version();
                        $scope.showRole = ShowHideRoles.showRole;

                        $scope.checkMail = checkMail;

                        $scope.newAcceptance = newAcceptance;

                        function checkMail($event) {
                            var button = $event.target;
                            disableButton(button, true);
                            mails.checkMail().then(function(res) {
                                if(res == "ok") {
                                    toastr.info("Есть новые письма. Для просмотра перейдите по <a href='/admin#/mailbox?_new=true&page=1'>ссылке</a>", "Оповещения");
                                } else if (res == "nothing") {
                                    toastr.info("Нету новых писем", "Оповещения", {"closeButton": true, "progressBar": true});
                                }
                                disableButton(button, false);
                            });
                        }

                        function newAcceptance($event) {
                            var button = $event.target;
                            disableButton(button, true);
                            console.log("new ACCEPTANCE");
                        }

                        function disableButton(element, comp) {
                            $(element).prop('disabled', comp);
                        }
                    }
                }
            }
        });
});