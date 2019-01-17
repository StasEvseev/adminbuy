/**
 * Created by user on 03.07.15.
 */

angular.module('waybill.service', ['core.service'])

.factory('waybills', function($http, BaseModelService, apiConfig) {
    var path = apiConfig.baseUrl + "/waybill";

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
        return $http.post(apiConfig.baseUrl + "/waybillbulk", data);
    };

    return child;
})

.factory('waybillstatus', function($http, apiConfig) {
    return {
        doStatus: function(id, number) {
            return $http.post(apiConfig.baseUrl + "/waybill/" + id + "/status", {data: {status: number}});
        }
    }
})

.factory('waybillprint', function($http, apiConfig) {
    return {
        print: function(id) {
            return $http.get(apiConfig.baseUrl + "/waybill/print/" + id);
        },
        printBulk: function(ids) {
            var par = {
                'ids': JSON.stringify(ids)
            };

            return $http.get(apiConfig.baseUrl + "/waybill/print_bulk", {params: par});
        }
    }
})

.factory("invoice_canon_items", function($http, apiConfig) {
        return {
            all: function(id, excl_ids) {
                var par = {};
                if (excl_ids) {
                    par['exclude_good_id'] = JSON.stringify(excl_ids);
                }
                return $http.get(apiConfig.baseUrl + "/invoice_canon/" + id + '/items', {params: par}).then(function(resp) {
                    return resp.data;
                });
            }
        }
})

.factory('waybillitems', function($http, apiConfig) {
        return {
            all: function(id) {
                return $http.get(apiConfig.baseUrl + "/waybill/" + id + '/items').then(function(resp) {
                    return resp.data.items;
                });
            }
        };
    });