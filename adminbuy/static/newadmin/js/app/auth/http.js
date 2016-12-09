/**
 * Created by user on 27.07.15.
 */

angular.module("auth.http", ["core.helpers"])

.config(function($httpProvider) {
    $httpProvider.interceptors.push('authInterceptor');
})

.factory('authInterceptor', function($rootScope, $q, $injector, $window, Base64, Device) {
    function statusBr(status) {
        /*
        * Уведомляем систему, о смене состояний(online/offline).
        * */
        $rootScope.$broadcast('online', {status: status});
    }
    return {
        // Add authorization token to headers
        request: function (config) {
            var principal = $injector.get("principal");
            config.headers = config.headers || {};
            if (principal.isAuthenticated()) {
                config.headers.Authorization = 'Basic ' + Base64.encode(principal.getToken() + ':' + 'unused');
            }
            config.headers.DeviceId = Device.getIfDefined();
            return config;
        },

        response: function(response) {
            statusBr(true);
            return response;
        },

        // Intercept 401s and redirect you to login
        responseError: function(response) {
            if(response.status === 401) {
                statusBr(true);
                var $state = $injector.get("$state");
                var principal = $injector.get("principal");
                principal.authenticate(null);
                $state.go('signin');
                return $q.reject(response);
            }
            else if (response.status === 403) {
                statusBr(true);
                var $state = $injector.get("$state");
                $state.go('index.accessdenied');
                return $q.reject(response);
            }

            else if (response.status == 0) {
                statusBr(false);
                return $q.reject(response);
            }
            else {
                statusBr(true);
                return $q.reject(response);
            }


        }
    };
});
