$scope.isCollapsed = true;

$scope.getPrice = function(event) {
    var btn = $(event.target);
    btn.button('loading');
    PriceHelper.get({
        'good_id': $scope.model.good.id,
        'price_post': $scope.model.price_with_NDS
    }, function(data) {
        btn.button('reset');
        $scope.model.price_recommendation = data.items;
        $scope.isCollapsed = false;
    });
};

$scope.compare_info = function(value, value1) {
    return parseFloat(value).toFixed(2) === parseFloat(value1).toFixed(2);
};

$scope.compare_warning = function(value, value1) {
    return parseFloat(value).toFixed(2) < parseFloat(value1).toFixed(2);
};

$scope.compare_success = function(value, value1) {
    return parseFloat(value).toFixed(2) > parseFloat(value1).toFixed(2);
};

$scope.setRec = function(price_retail, price_gross) {
    $scope.model.price_retail = price_retail;
    $scope.model.price_gross = price_gross;
};