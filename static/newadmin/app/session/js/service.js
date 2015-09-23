/**
 * Created by user on 22.09.15.
 */

angular.module("session.service", ['indexedDB'])

.factory("SessionService", function($indexedDB, $http, $q, $window) {
    var OBJECT_STORE_NAME = 'session_items';
    var OBJECT_WD_NAME = "workdays";
    var TOKEN_DAY = "WORK_DAY";
    return {

        beginWorkDay: function(date, username) {
            var self = this;
            var q = $q.defer();
            $indexedDB.openStore(OBJECT_WD_NAME, function(store) {
                var wd = {
                    date_start: date,
                    date_end: '',
                    username: username
                };
                store.insert(wd).then(function(id) {
                    self.setWork(id[0]);
                    q.resolve();
                });
            });

            return q.promise;
        },

        getOpenWorkDay: function() {
            var q = $q.defer();
            $indexedDB.openStore(OBJECT_WD_NAME, function(store) {
                store.findBy('date_end_idx', '').then(function(res) {
                    q.resolve({res: res, store: store});
                });
            });

            return q.promise;
        },

        hasOpenWorkDay: function() {
            var q = $q.defer();

            this.getOpenWorkDay().then(function(resp) {
                if (angular.isUndefined(resp['res'])) {
                    q.resolve(false);
                } else {
                    q.resolve(true);
                }
            });

            return q.promise;
        },

        endWorkDay: function() {
            var q = $q.defer();
            var self = this;
            self.getOpenWorkDay().then(function(resp) {
                var workday = resp['res'];
                var store = resp['store'];
                workday.date_end = new Date();

                store.upsert(workday);
                self.deleteWork();
                q.resolve();
            });

            return q.promise;
        },

        setWork: function(id) {
            $window.localStorage[TOKEN_DAY] = id;
        },

        deleteWork: function() {
            delete $window.localStorage[TOKEN_DAY];
        },

        isWork: function(){
            if ($window.localStorage[TOKEN_DAY]) {
                return true;
            }
            return false;
        },

        syncSessionItems: function() {
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
                }).catch(function(er) {
                    q.reject(er);
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