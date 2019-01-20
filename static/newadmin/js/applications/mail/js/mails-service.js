/**
 * Created by user on 02.07.15.
 */

angular.module('mails.service', ['core.utils'])

.factory('mails', function($http, $q, remoteHelper, apiConfig) {
    var path = apiConfig.baseUrl + "/mail";
    var cnt = 0;
    var items = [];
    var items_id = [];
    var items_new = [];
    var current_id = undefined;

    var factory = {};

    factory.handle_mail = function(id, index, action) {
        return $http.post(apiConfig.baseUrl + "/mail/" + id, {index: index, action: action});
    };

    factory.checkMail = function() {
        return $http.post(apiConfig.baseUrl + "/mail").then(function(resp) {
            return resp.data;
        });
    };

    factory.checkMailAndLoadItems = function($stateParams) {
        var q = $q.defer(),
            self = this;

        self.checkMail().then(function (res) {
            self.filterToStateParams($stateParams).then(function(items) {
                q.resolve([res, items]);
            });
        }).catch(function() {
            q.reject();
        });

        return q.promise;
    };

    factory.fetch = function() {
        return $http.get(apiConfig.baseUrl + "/mail", {params: {'_new': true}}).then(function(resp) {
            items_new = resp.data.items;
        }, function(resp) {
            var isOnline = true;
            if (resp.status == 0) {isOnline = false; items_new = [];}
            return isOnline;
        });
    };

    factory.add = function(item) {
        items_new.push(item);
    };

    factory.remove = function(id) {
        items_new = _.filter(items_new, function(item) {
            if (item.id != id) return true;
        });
    };

    factory.all_new = function() {
        return items_new;
    };

    factory.countNew = function() {
        return items_new.length;
    };

    factory.setCurrent = function(item) {
        current_id = item.id;
    };

    factory.getById = function(id) {
        return remoteHelper.itemById(path, id);
    };

    factory.hasNext = function() {
        if (!angular.isUndefined(current_id) && [-1, 9].indexOf(items_id.indexOf(current_id)) === -1) {
            return true;
        }
    };

    factory.hasPrev = function() {
        if (!angular.isUndefined(current_id) && [-1, 0].indexOf(items_id.indexOf(current_id)) === -1) {
            return true;
        }
    };

    factory.getNext = function() {
        if(factory.hasNext()) {
            return items_id[items_id.indexOf(current_id) + 1];
        }
    };
    factory.getPrev = function() {
        if(factory.hasPrev()) {
            return items_id[items_id.indexOf(current_id) - 1];
        }
    };

    factory.filterToStateParams = function(stateParams) {
        return factory.filter(stateParams.filter, stateParams.page, stateParams.count, stateParams._new)
    };

    factory.filter = function(text, page, count, _new) {
        var params = remoteHelper.createParams(text, 'title', page, count);
        if (_new) {
            params['_new'] = _new;
        }

        return remoteHelper.filterItems(path, params).then(function(resp) {
            cnt = resp.data.max;
            items = resp.data.items;
            items_id = _.map(items, function(item) {return item.id});
            return items;
        }, function() {
            return [];
        });
    };

    factory.count = function() {
        return cnt;
    };

    return factory;
});

