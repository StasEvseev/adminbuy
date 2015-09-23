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
        url: '/session',
        resolve: {
            isWork: function($state, $rootScope, SessionService) {
                if ($rootScope.toState.name != 'index.session.menu' && !SessionService.isWork()) {
                    $state.go('index.session.menu');
                }
            }
        }
    })

    .state('index.session.menu', {
        url: '/menu',
        views: {
            'content@index': {
                templateUrl: "static/newadmin/app/session/template/menu.html",
                controller: function($scope, $modal, SessionService) {

                    $modal.open({
                        templateUrl: "static/newadmin/app/session/template/menumodal.html",
                        controller: function($scope, $state, $modalInstance, principal) {
                            $scope.logout = function() {
                                principal.authenticate();
                                $state.go("signin").then(function() {
                                    $modalInstance.dismiss('cancel');
                                });
                            };

                            $scope.openWorkday = function() {
                                SessionService.hasOpenWorkDay().then(function(result) {
                                    if (result === true) {
                                        if(confirm("Для того, чтобы открыть новый рабочий день, следует закрыть старый.", "Закрытие старого дня.")) {
                                            SessionService.endWorkDay().then(function() {
                                                $scope.$digest();
                                            });
                                        }
                                    } else {
                                        SessionService.beginWorkDay($scope.date, principal.getUser()).then(function() {

                                            $state.go('index.session.view').then(function() {
                                                $modalInstance.dismiss('cancel');
                                            });
                                        });
                                    }
                                });

                            };
                            $scope.hasOpenWorkDay = false;
                            SessionService.hasOpenWorkDay().then(function(result) {
                                $scope.hasOpenWorkDay = result;
                            });

                            $scope.date = new Date();
                        },
                        backdrop: "static",
                        size: "lg"

                    });

                }
            }
        }
    })

    .state('index.session.view', {
        url: "?filter&page",
        views: {
            'content@index': {
                templateUrl: "static/newadmin/app/session/template/view.html",
                controller: function($scope, $state, $rootScope, $http, $window, $timeout, goods, hIDScanner, SessionService) {
                    $scope.items = [];
                    hIDScanner.initialize();

                    SessionService.getOpenWorkDay().then(function(resp) {
                        var day = resp['res'];
                        $scope.date = day.date_start;
                    });

                    SessionService.getAllItem(SessionService.getWork()).then(function(results) {
                        // Update scope
                        $scope.items = results;
                    });

                    $scope.$on('$destroy', function() {
                        hIDScanner.uninitialize();
                    });

                    $scope.closeWorkDay = function() {
                        SessionService.endWorkDay().then(function() {
                            $state.go('index.session.menu');
                        });
                    };

                    $scope.sync = function() {
                        SessionService.syncSessionItems();
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
                            count: 1,
                            work_id: SessionService.getWork()
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