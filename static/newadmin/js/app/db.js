/**
 * Created by user on 22.09.15.
 */

angular.module('dbApp', ['indexedDB'])
.constant('DBSettings', {
    DBNAME: "myDB__test9"
})

.config(function ($indexedDBProvider, DBSettings) {
    $indexedDBProvider.connection(DBSettings.DBNAME).upgradeDatabase(3, function(event, db, tx) {
        var objStore = db.createObjectStore('workdays', { autoIncrement : true, keyPath: 'id'});
        objStore.createIndex('username_idx', 'username', {unique: false});
        objStore.createIndex('date_start_idx', 'date_start', {unique: false});
        objStore.createIndex('date_end_idx', 'date_end', {unique: false});
    });
})

.config(function ($indexedDBProvider, DBSettings) {
    $indexedDBProvider.connection(DBSettings.DBNAME).upgradeDatabase(1, function(event, db, tx) {
        var objStore = db.createObjectStore('session_items', { autoIncrement : true, keyPath: 'id'});
        objStore.createIndex('is_sync_idx', 'is_sync', {unique: false});
        objStore.createIndex('work_id_idx', 'work_id', {unique: false});
    });
})

.config(function ($indexedDBProvider, DBSettings) {
    $indexedDBProvider.connection(DBSettings.DBNAME).upgradeDatabase(2, function(event, db, tx) {
        var objStore = db.createObjectStore('users', { autoIncrement : true, keyPath: 'id'});
        objStore.createIndex('name_idx', 'name', {unique: true});
    });
});