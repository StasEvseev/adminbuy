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
                    is_sync: 0,
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

        getWork: function() {
            return parseInt($window.localStorage[TOKEN_DAY]);
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

        getDataToSync: function() {
            //Выбираем те workday у которых is_sync равен 0.
            //Далее выбираем связанные session_items у которых work_id равен выбранным workdays.
            var result = [];
            var queue_q = [];
            var q = $q.defer();
            $indexedDB.openStore(OBJECT_WD_NAME, function(store) {
                store.eachBy('is_sync_idx', {beginKey: 0, endKey: 0}).then(function(workday_items) {

                    for (var j = 0; j < workday_items.length; j++) {
                        var work = workday_items[j];

                        (function(w) {
                            var q_sub = $q.defer();
                            queue_q.push(q_sub.promise);
                            $indexedDB.openStore(OBJECT_STORE_NAME, function(store) {
                                w['items'] = [];
                                result.push(w);
                                var query = store.query().$index('my_cool_idx').$eq([0, w.id]);
                                (function(defer, query_in, work) {
                                    store.eachWhere(query_in).then(function(items) {
                                        work['items'] = items;
                                        defer.resolve();
                                    });
                                })(q_sub, query, w);

                            });

                        })(work);
                    }

                    $q.all(queue_q).then(function() {
                        q.resolve(result);
                    });
                });
            });

            return q.promise;
        },

        saveSyncData: function(result) {
            var q = $q.defer();
            var queue_q = [];
            for (var i = 0; i < result.length; i++) {
                item = result[i];

                var q_s = $q.defer();
                queue_q.push(q_s.promise);

                (function(q, itm) {
                    $indexedDB.openStores([OBJECT_WD_NAME, OBJECT_STORE_NAME], function(storeWD, storeItems) {

                        var items = _.map(itm['items'], function(item) {
                            item.is_sync = 1;
                            return item;
                        });

                        storeItems.upsert(items).then(function () {
                            if(itm.date_end) {
                                itm.is_sync = 1;
                                storeWD.upsert(itm);
                            }
                            q.resolve();
                        });
                    });
                })(q_s, item);
            }

            $q.all(queue_q).then(function() {
                q.resolve();
            });

            return q.promise;
        },

        syncSession: function() {
            var self = this;
            var q = $q.defer();
            //Синхронизируем записи workday и session_items
            //Выбираем данные для синхронизации
            //После успешной синхронизации, выставляем флаг is_sync у тех workdays у которых date_end не пустой.
            this.getDataToSync().then(function(result) {
                console.log("Data to sync", result);

                $http.post('/api/syncSession', {data: {items: result}}).then(function(resp) {

                    self.saveSyncData(result).then(function() {
                        q.resolve();
                    });

                }).catch(function(resp) {
                    q.reject();
                });
            });

            return q.promise;
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
        getAllItem: function(work_id) {
            var q = $q.defer();
            var OBJECT_STORE_NAME = 'session_items';
            $indexedDB.openStore(OBJECT_STORE_NAME, function(store) {
                store.eachBy('work_id_idx', {beginKey: work_id, endKey: work_id}).then(function(results) {
                    q.resolve(results);
                });
            });

            return q.promise;
        }
    }
});
