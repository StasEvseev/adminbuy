/**
 * Created by user on 03.07.15.
 */

angular.module('waybill.service', ['core.service'])

.factory('waybills', function($http, BaseModelService) {
    var path = 'api/waybill';

    var child = Object.create(BaseModelService);
    child._getPath = function () {
        return path;
    };

    child.filter = function(text, page, count) {
        return BaseModelService.filter.call(this, text, page, count).then(function(resp) {
            return resp.data.items;
        });
    };

    child.createBulk = function(data) {
        return $http.post("/api/waybillbulk", data);
    };

    return child;
})

.factory('waybillprint', function($http) {
    return {
        print: function(id) {
            return $http.get("/api/waybill/print/" + id);
        }
    }
})

.factory("invoice_canon_items", function($http) {
        return {
            all: function(id, excl_ids) {
                var par = {};
                if (excl_ids) {
                    par['exclude_good_id'] = JSON.stringify(excl_ids);
                }
                return $http.get('api/invoice_canon/' + id + '/items', {params: par}).then(function(resp) {
                    return resp.data;
                });
            }
        }
})

.factory('waybillitems', function($http) {
        return {
            all: function(id) {
                return $http.get('api/waybill/' + id + '/items').then(function(resp) {
                    return resp.data.items;
                });
            }
        };
    });