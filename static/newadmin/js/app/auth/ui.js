/**
 * Created by user on 27.07.15.
 */
angular.module('auth.ui', ['ui.router'])

.factory('principal', ['$q', '$http', '$timeout', '$window',
  function($q, $http, $timeout, $window) {
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
      deleteToken: function() {
          delete $window.localStorage.token;
      },

      authenticate: function(identity) {
          var self = this;
          var _identity = identity;
          var q;

          if (identity) {
              q = $q.defer();

              $http.post("/api/auth", {user: identity.login, password: identity.password}).then(function(resp) {
                  self.setToken(resp.data.token);
                  q.resolve();
              }, function(resp) {
                  self.deleteToken();
                  _identity = undefined;
                  q.reject();
              });

              return q.promise;
          } else {
              self.deleteToken();
              self.deleteIdentity();
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

          $http.get("/api/identity")
                                  .success(function(data){
                                    self.setIdentity(data.identity);
//                                    _identity = data.identity;
//                                    _authenticated = true;
                                    deferred.resolve(_identity);
                                }).error(function(data) {
                  self.deleteIdentity();
                  self.deleteToken();
                  deferred.resolve(_identity);
              });

        // for the sake of the demo, fake the lookup by using a timeout to create a valid
        // fake identity. in reality,  you'll want something more like the $http request
        // commented out above. in this example, we fake looking up to find the user is
        // not logged in

//        $timeout(function() {
////          self.authenticate(null);
//        deferred.resolve(_identity);
//        }, 100);

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
                        if (isAuthenticated) $state.go('index.accessdenied'); // user is signed in but not authorized for desired state
                        else {
                            // user is not authenticated. stow the state they wanted before you
                            // send them to the signin state, so you can return them when you're done
                            $rootScope.returnToState = $rootScope.toState;
                            $rootScope.returnToStateParams = $rootScope.toStateParams;

                            // now, send them to the signin state so they can log in
                            $state.go('signin');
                        }
                    }

//                    if ($rootScope.toState.name != "signin" && $rootScope.toState.name != "register" && !isAuthenticated) {
//
//                        // user is not authenticated. stow the state they wanted before you
//                        // send them to the signin state, so you can return them when you're done
//                        $rootScope.returnToState = $rootScope.toState;
//                        $rootScope.returnToStateParams = $rootScope.toStateParams;
//
//                        // now, send them to the signin state so they can log in
//                        $state.go('signin');
//                    }
                });
            }
        };
    }
])

.run(['$rootScope', '$state', '$stateParams', 'authorization', 'principal', '$timeout',
    function($rootScope, $state, $stateParams, authorization, principal, $timeout) {

      $rootScope.$on('$stateChangeStart', function(event, toState, toStateParams) {
        // track the state the user wants to go to; authorization service needs this
        $rootScope.toState = toState;
        $rootScope.toStateParams = toStateParams;
        // if the principal is resolved, do an authorization check immediately. otherwise,
        // it'll be done when the state it resolved.
          if ($rootScope.toState.name != "signin" && $rootScope.toState.name != "register") {
            if (!principal.isAuthenticated()) {

//                authorization.authorize();
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



