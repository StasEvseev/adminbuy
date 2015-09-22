/**
 * Created by Stanislav on 12.09.2015.
 */

angular.module("session.module", ['ui.router', 'core.service', 'core.controllers', 'good.service', 'session.service'])

.config(function($stateProvider) {
    $stateProvider.state('index.session', {
        data: {
             roles: ['vendor']
        },
        abstract: true,
        url: '/session'
    })
    .state('index.session.view', {
        url: "?filter&page",
        views: {
            'content@index': {
                templateUrl: "static/newadmin/app/session/template/view.html",
                controller: function($scope, $rootScope, $http, $window, $timeout, goods, hIDScanner, SessionService) {
                    $scope.items = [];
                    hIDScanner.initialize();

                    SessionService.getAllItem().then(function(results) {
                        // Update scope
                        $scope.items = results;
                    });

                    $scope.$on('$destroy', function() {
                        hIDScanner.uninitialize();
                    });

                    $scope.sync = function() {
                        SessionService.sync();
                    };

                    var checkMap = {
                        1: "Продажа",
                        2: "Возврат"
                    };

                    $rootScope.$on("hidScanner::scanned", function(event, barcode) {
                        var item = {
                            barcode: barcode.barcode,
                            operation: $scope.checkModel,
                            checkModel: checkMap[$scope.checkModel],
                            datetime: new Date(),
                            is_sync: 0,
                            count: 1
                        };

                        SessionService.insertItem(item).then(function(item) {
                            $scope.items.push(item);
                        }).catch(function(err) {
                            console.error(err);
                        });
                    });

                    $scope.checkModel = 1;
                }
            }
        }
    })}
);