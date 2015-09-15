/**
 * Created by Stanislav on 12.09.2015.
 */

angular.module("session.module", ['ui.router', 'core.service', 'core.controllers', 'good.service'])

.config(function($stateProvider) {
    $stateProvider.state('index.session', {
        abstract: true,
        url: '/session'
    })
    .state('index.session.view', {
        url: "?filter&page",
        views: {
            'content@index': {
                templateUrl: "static/newadmin/app/session/template/view.html",
                controller: function($scope, $rootScope, $window, $timeout, goods, hIDScanner) {
                    hIDScanner.initialize();

                    $rootScope.$on("hidScanner::scanned", function(event, barcode) {
                        $scope.items.push({'barcode': barcode.barcode, checkModel: $scope.checkModel});
                    });
                    $scope.getLocation = function(value) {
                        return goods.filter(value).then(function(resp) {
                            return resp;
                        })
                    };

                    $scope.add = function() {
                        $scope.items.push({});
                    };

                    $scope.checkModel = 'Продажа';

                    $scope.items = [];
                }
            }
        }
    })}
);