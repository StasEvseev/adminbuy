/**
 * Created by user on 27.07.15.
 */

angular.module("auth.http", ["core.helpers"])

.config(function($httpProvider) {
    $httpProvider.interceptors.push('authInterceptor');
})

.factory('authInterceptor', function($q, $injector, $window, Base64) {
    return {
        // Add authorization token to headers
        request: function (config) {
            var principal = $injector.get("principal");
            config.headers = config.headers || {};
            if (principal.isAuthenticated()) {
                config.headers.Authorization = 'Basic ' + Base64.encode(principal.getToken() + ':' + 'unused');
            }
            return config;
        },

        // Intercept 401s and redirect you to login
        responseError: function(response) {
            if(response.status === 401) {
                var $state = $injector.get("$state");
                var principal = $injector.get("principal");
                principal.authenticate(null);
                $state.go('signin');
                return $q.reject(response);
            }
            else if (response.status === 403) {
                var $state = $injector.get("$state");
                $state.go('index.accessdenied');
                return $q.reject(response);
            }
            else {
                return $q.reject(response);
            }
        }
    };
});