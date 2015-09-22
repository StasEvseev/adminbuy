/**
 * Created by user on 22.09.15.
 */

angular.module('dbApp', ['indexedDB'])
.constant('DBSettings', {
    DBNAME: "myDB__test7"
})

.config(function ($indexedDBProvider, DBSettings) {
    $indexedDBProvider.connection(DBSettings.DBNAME).upgradeDatabase(1, function(event, db, tx) {
        var objStore = db.createObjectStore('session_items', { autoIncrement : true, keyPath: 'id'});
        objStore.createIndex('is_sync_idx', 'is_sync', {unique: false});
    });
})

.config(function ($indexedDBProvider, DBSettings) {
    $indexedDBProvider.connection(DBSettings.DBNAME).upgradeDatabase(2, function(event, db, tx) {
        var objStore = db.createObjectStore('users', { autoIncrement : true, keyPath: 'id'});
        objStore.createIndex('name_idx', 'name', {unique: true});
    });
});