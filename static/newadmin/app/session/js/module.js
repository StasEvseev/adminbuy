/**
 * Created by Stanislav on 12.09.2015.
 */

angular.module("session.module", ['ui.router', 'core.service', 'core.controllers', 'good.service'])

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
                controller: function($scope, $rootScope, $http, $window, $timeout, goods, hIDScanner, $indexedDB, Device) {
                    $scope.items = [];
                    hIDScanner.initialize();

                    var OBJECT_STORE_NAME = 'session_items';
                    $indexedDB.openStore(OBJECT_STORE_NAME, function(store) {
                        store.getAll().then(function(results) {
                          // Update scope
                            $scope.items = results;
                        });
                    });

                    $scope.$on('$destroy', function() {
                        hIDScanner.uninitialize();
                    });

                    $scope.sync = function() {

                        $indexedDB.openStore(OBJECT_STORE_NAME, function(store) {

                            store.eachBy('is_sync_idx', {beginKey: 0, endKey: 0}).then(function(res) {
                                console.log("Row to sync", res);
                                $http.post('/api/syncSession', {data: {items: res}}).then(function(resp) {

                                    $indexedDB.openStore(OBJECT_STORE_NAME, function(store) {
                                        var items = _.map(res, function(item) {
                                            item.is_sync = 1;
                                            return item;
                                        });
                                        store.upsert(items);
                                    });
                                }).catch(function(resp) {
                                    debugger
                                });
                            })});
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

                        $indexedDB.openStore(OBJECT_STORE_NAME, function(store) {
                            store.insert(item).then(function(res) {
                                item['id'] = res[0];
                               $scope.items.push(item);
                            }).catch(function(er) {
                                console.error(er);
                            });
                        });
                    });

                    $scope.checkModel = 1;
                }
            }
        }
    })}
);