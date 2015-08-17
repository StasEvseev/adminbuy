app.controller('{{ modal_cntr }}', function($scope, $rootScope, object, $timeout, $modalInstance{{depend|safe}}
) {
    $scope.model = {};
    $scope.errors = {};
    $scope.validate = {};

    $scope.resource = {{res_get_all}}.meth;
    $scope.{{dict}} = {{res}}.meth;

    $scope.$watch('model.{{dict}}', function(value) {
        if (value) {
            $scope.resourceparams = {
                'inner_id': $scope.model.{{dict}}.id,
                'sort_course': 'asc',
                'sort_field': 'id'
            };
            $timeout(function() {
                        $scope.rel();
                    }, 500);
        }
    });

    var setError = function(attr, message) {
        if (message) {
            $scope.errors[attr] = true;
            $scope.validate[attr] = message;
        } else {
            $scope.errors[attr] = false;
            $scope.validate[attr] = message;
        }
    };

    $scope.ok = function () {
        $modalInstance.close($scope.multiselects);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});