$scope.{{ import_id }}openAdd = function() {

    var modalInstance = $modal.open({
        templateUrl: '{{ import_modal_id }}',
        controller: '{{ import_modal_ctrl }}',
        size: 'lg',
        backdrop: 'static',
        resolve: {
            object: function() {
                return $scope;
            }
        }
    });

    modalInstance.result.then(function (select) {
        ITEMS{{tab_id}} = $scope.items.{{ tab_id }}ITEMS.concat(select);
        console.log(select);
        $scope.items.{{ tab_id }}ITEMS = ITEMS{{tab_id}};

    }, function () {
        console.log("THEN2");
    });
};