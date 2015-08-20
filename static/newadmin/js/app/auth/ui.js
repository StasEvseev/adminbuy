/**
 * Created by user on 27.07.15.
 */
angular.module('auth.ui', ['ui.router'])

.factory('principal', ['$q', '$http', '$timeout', '$window',
  function($q, $http, $timeout, $window) {
    var _identity = undefined;

    return {
      isAuthenticated: function() {
        return angular.isDefined(this.getToken());
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

//      registration: function(identity) {
//          var self = this;
//          var q = $q.defer();
//          $http.post("/api/registration", {
//              login: identity.login, email: identity.email,
//              password: identity.password, retypepassword: identity.retypepassword
//          }).then(function(resp) {
//              self.setToken(resp.data.token);
//              q.resolve();
//          }, function() {
//              q.reject(resp);
//          });
//
//          return q.promise;
//      },

      authenticate: function(identity) {
          var self = this;
          _identity = identity;
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
          }
      },
      identity: function(force) {
        var deferred = $q.defer();

        if (force === true) _identity = undefined;

        // check and see if we have retrieved the identity data from the server. if we have, reuse it by immediately resolving
        if (angular.isDefined(_identity)) {
          deferred.resolve(_identity);

          return deferred.promise;
        }

        // for the sake of the demo, fake the lookup by using a timeout to create a valid
        // fake identity. in reality,  you'll want something more like the $http request
        // commented out above. in this example, we fake looking up to find the user is
        // not logged in
        var self = this;
        $timeout(function() {
//          self.authenticate(null);
        deferred.resolve(_identity);
        }, 100);

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

                    if ($rootScope.toState.name != "signin" && $rootScope.toState.name != "register" && !isAuthenticated) {

                        // user is not authenticated. stow the state they wanted before you
                        // send them to the signin state, so you can return them when you're done
                        $rootScope.returnToState = $rootScope.toState;
                        $rootScope.returnToStateParams = $rootScope.toStateParams;

                        // now, send them to the signin state so they can log in
                        $state.go('signin');
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
          }

      });
    }
  ]);



