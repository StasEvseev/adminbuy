/**
 * Created by user on 22.09.15.
 */

angular.module("session.service", ['indexedDB'])

.factory("SessionService", function($indexedDB, $http, $q) {
    var OBJECT_STORE_NAME = 'session_items';
    return {
        sync: function() {
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
                })
            });
        },
        insertItem: function(item) {
            var q = $q.defer();
            $indexedDB.openStore(OBJECT_STORE_NAME, function(store) {
                store.insert(item).then(function(res) {
                    q.resolve(item);
//                   $scope.items.push(item);
                }).catch(function(er) {
                    q.reject(er);
//                    console.error(er);
                });
            });
            return q.promise;
        },
        getAllItem: function() {
            var q = $q.defer();
            var OBJECT_STORE_NAME = 'session_items';
            $indexedDB.openStore(OBJECT_STORE_NAME, function(store) {
                store.getAll().then(function(results) {
                    q.resolve(results);
                });
            });

            return q.promise;
        }
    }
});