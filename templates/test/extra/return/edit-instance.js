if($scope.model.status == '{{status_1}}') {
    $scope.extra_flds.btn_1_show = true;
}
else if ($scope.model.status == '{{status_2}}') {
    $scope.extra_flds.btn_2_show = true;
    $scope.extra_flds.btn_4_show = true;
} else if ($scope.model.status == '{{status_3}}') {
    $scope.extra_flds.btn_3_show = true;
    $scope.extra_flds.btn_5_show = true;
}