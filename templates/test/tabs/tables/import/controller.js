app.controller('{{ modal_cntr }}', function($scope, $rootScope, object, $modalInstance{{depend|safe}}
) {
//    var object = {};
    $scope.model = {};
    $scope.errors = {};
    $scope.validate = {};

    $scope.resource = {{res_get_all}}.meth;
    $scope.resourceparams = {
        'inner_id': object.model.pointsale_from_id,
        'sort_course': 'asc',
        'sort_field': 'id'
    };

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