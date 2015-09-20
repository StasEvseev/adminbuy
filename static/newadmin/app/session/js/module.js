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
                controller: function($scope, $rootScope, $http, $window, $timeout, goods, hIDScanner, $indexedDB) {
                    $scope.items = [];
                    hIDScanner.initialize();

                    var OBJECT_STORE_NAME = 'session_items';
                    var myObjectStore;
                    $indexedDB.openStore(OBJECT_STORE_NAME, function(store) {
                        myObjectStore = store;

                        myObjectStore.getAll().then(function(results) {
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
                                $http.post('/api/syncSession', {data: {items: res}});
                            })});

                        //var myQuery = $indexedDB.queryBuilder().$index('is_sync_idx').compile();
                        //myObjectStore.each(myQuery).then(function(cursor){
                        //    debugger
                        //    cursor.key;
                        //    cursor.value;
                        //});



                    };

                    $rootScope.$on("hidScanner::scanned", function(event, barcode) {
                        var item = {
                            barcode: barcode.barcode,
                            checkModel: $scope.checkModel,
                            datetime: new Date(),
                            is_sync: 0
                        };

                        myObjectStore.insert(item).then(function() {
                           $scope. items.push(item);
                        }).catch(function(er) {
                            console.error(er);
                        });
                    });

                    $scope.checkModel = 'Продажа';
                }
            }
        }
    })}
);