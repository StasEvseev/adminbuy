/**
 * Created by user on 27.07.15.
 */
angular.module('auth.ui', ['ui.router', 'indexedDB'])

.factory('principal', ['$q', '$http', '$timeout', '$window', '$indexedDB', 'apiConfig',
    function($q, $http, $timeout, $window, $indexedDB, apiConfig) {
        var _identity = undefined, _authenticated = false;

        return {
            isIdentityResolved: function() {
                return angular.isDefined(this.getIdentity());
            },
            isInRole: function(role) {
                var _identity = this.getIdentity();
                var _authenticated = this.isAuthenticated();
                if (!_authenticated || !_identity) return false;
                return _identity.indexOf(role) != -1;
            },
            isInAnyRole: function(roles) {
                var _identity = this.getIdentity();
                var _authenticated = this.isAuthenticated();
                if (!_authenticated || !_identity) return false;

                for (var i = 0; i < roles.length; i++) {
                    if (this.isInRole(roles[i])) return true;
                }

                return false;
            },

            permissionRoles: function(roles) {
                if (roles && roles.length > 0 && !this.isInAnyRole(roles)) {
                    return false;
                }
                return true;
            },

            isAuthenticated: function() {
                return angular.isDefined(this.getToken());
            },

            getIdentity: function() {
                if ($window.localStorage.identity) {
                    return JSON.parse($window.localStorage.identity);
                }
            },

            setIdentity: function(identity) {
                $window.localStorage.identity = JSON.stringify(identity);
            },

            deleteIdentity: function() {
                delete $window.localStorage.identity;
            },

            getToken: function() {
                return $window.localStorage.token;
            },
            setToken: function(token) {
                $window.localStorage.token = token;
            },
            setUser: function(name) {
                $window.localStorage.username = name;
            },
            getUser: function() {
                return $window.localStorage.username;
            },
            deleteUser: function() {
                delete $window.localStorage.username;
            },
            deleteToken: function() {
                delete $window.localStorage.token;
            },

            authenticate: function(identity) {
                var self = this;
                var q;

                if (identity) {
                    var user = {
                        name: identity.login,
                        password: identity.password
                    };
                    q = $q.defer();

                    $http({
                        method: 'POST',
                        url: apiConfig.baseUrl + "/api/auth",
                        data: {user: user.name, password: user.password}
                    }).then(successAuth, failureAuth);

                    return q.promise;
                } else {
                    self.deleteToken();
                    self.deleteIdentity();
                }

                function successAuth(resp) {
                    console.info("Success Auth.");
                    var user = {
                        name: identity.login,
                        password: identity.password,
                        token: resp.data.token
                    };
                    var q2 = $q.defer();

                    $indexedDB.openStore('users', function(store) {

                        store.findBy('name_idx', user.name).then(function(usr) {
                            console.info("Get user after success auth. " + usr);

                            if (angular.isUndefined(usr)) {
                                store.insert(user);
                            } else {
                                usr.token = resp.data.token;
                                usr.password = user.password;
                                store.upsert(usr);
                            }

                            q2.resolve();

                        });
                    });

                    q2.promise.then(function() {
                        self.setUser(user.name);
                        self.setToken(resp.data.token);
                        self.identity().then(function() {
                            q.resolve();
                        });
                    });
                }

                function failureAuth(resp) {
                    console.info("Failure Auth.");
                    if (resp.status == 0) {
                        $indexedDB.openStore('users', function(store) {
                            store.findBy('name_idx', user.name).then(function(usr) {
                                if (angular.isUndefined(usr) || usr.password != user.password) {
                                    self.deleteToken();
                                    self.deleteUser();
                                    q.reject("В локальной базе не найден пользователь " + user.name);
                                } else {
                                    self.setToken(usr.token);
                                    self.setUser(user.name);
                                    self.identity().then(function() {
                                        q.resolve();
                                    });

                                }
                            });
                        });
                    } else {
                        self.deleteToken();
                        self.deleteUser();
                        q.reject(resp.data.message);
                    }
                }
            },
            identity: function(force) {
                var self = this;
                var deferred = $q.defer();
                var _identity = this.getIdentity();

                if (force === true) _identity = undefined;


                // check and see if we have retrieved the identity data from the server. if we have, reuse it by immediately resolving
                if (angular.isDefined(_identity)) {
                    deferred.resolve(_identity);

                    return deferred.promise;
                }

                //Пытаемся получить identity онлайн, если отсутствует сеть - берем из локальной базы
                //
                $http.get(apiConfig.baseUrl + "/api/identity").success(function(data){

                    var q = $q.defer();

                    $indexedDB.openStore('users', function(store) {
                        store.findBy('name_idx', self.getUser()).then(function(usr) {
                            usr.identity = data.identity;
                            store.upsert(usr);
                            q.resolve(data.identity);
                        });
                    });

                    q.promise.then(function(identity) {
                        self.setIdentity(identity);
                        deferred.resolve(self.getIdentity());
                    });

                }).error(function(resp) {

                    function Fail() {
                        self.deleteIdentity();
                        self.deleteToken();
                        deferred.resolve(undefined);
                    }

                    if (resp == null && self.getUser()) {

                        $indexedDB.openStore('users', function(store) {
                            store.findBy('name_idx', self.getUser()).then(function(usr) {
                                if (!angular.isUndefined(usr)) {
                                    self.setIdentity(usr.identity);
                                    deferred.resolve(self.getIdentity());
                                } else {
                                    Fail();
                                }
                            });
                        });

                    } else {
                        Fail();
                    }
                });

                return deferred.promise;
            }
        };
    }
])

.factory('authorization', ['$rootScope', '$state', 'principal',
    function($rootScope, $state, principal) {
        return {
            authorize: function() {
                return principal.identity().then(function() {
                    var isAuthenticated = principal.isAuthenticated();

                    if ($rootScope.toState.name != "signin" && $rootScope.toState.name != "register" &&
                        $rootScope.toState.data &&
                        $rootScope.toState.data.roles && $rootScope.toState.data.roles.length > 0 &&
                        !principal.isInAnyRole($rootScope.toState.data.roles)) {
                        if (isAuthenticated)
                            $state.go('index.accessdenied'); // user is signed in but not authorized for desired state
                        else {
                            // user is not authenticated. stow the state they wanted before you
                            // send them to the signin state, so you can return them when you're done
                            $rootScope.returnToState = $rootScope.toState;
                            $rootScope.returnToStateParams = $rootScope.toStateParams;

                            // now, send them to the signin state so they can log in
                            $state.go('signin');
                        }
                    }
                });
            }
        };
    }
])

.run(['$rootScope', '$state', '$stateParams', 'authorization', 'principal', '$timeout',
    function($rootScope, $state, $stateParams, authorization, principal, $timeout) {

        $rootScope.$on('$stateChangeStart', function(event, toState, toStateParams) {
            // track the state the user wants to go to; authorization service needs this
            $('.qtip').qtip('hide');

            $rootScope.toState = toState;
            $rootScope.toStateParams = toStateParams;
            // if the principal is resolved, do an authorization check immediately. otherwise,
            // it'll be done when the state it resolved.
            if ($rootScope.toState.name != "signin" && $rootScope.toState.name != "register") {
                if (!principal.isAuthenticated()) {

                    if ($state.current.name == 'register' || $state.current.name == "signin") {
                        event.preventDefault();
                    }

                    if (!$rootScope.$$phase) {
                        $rootScope.$apply(function() {
                            $state.go('signin');
                        });
                    } else {
                        $timeout(function() {
                            $rootScope.$apply(function() {
                                $state.go('signin');
                            });
                        }, 0)
                    }

                }
                if (principal.isIdentityResolved()) {
                      authorization.authorize();
                }
            }

        });
    }
]);



