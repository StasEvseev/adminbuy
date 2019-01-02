/**
 * Created by user on 03.07.15.
 */

angular.module('waybill.service', ['core.service'])

.factory('waybills', function($http, BaseModelService) {
    var path = 'http://127.0.0.1:8000/api/waybill/';

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
        return $http.post("http://127.0.0.1:8000/api/waybillbulk/", data);
    };

    return child;
})

.factory('waybillstatus', function($http) {
    return {
        doStatus: function(id, number) {
            return $http.post("http://127.0.0.1:8000/api/waybill/" + id + "/status/", {data: {status: number}});
        }
    }
})

.factory('waybillprint', function($http) {
    return {
        print: function(id) {
            return $http.get("http://127.0.0.1:8000/api/waybill/print/" + id + "/");
        },
        printBulk: function(ids) {
            var par = {
                'ids': JSON.stringify(ids)
            };

            return $http.get("http://127.0.0.1:8000/api/waybill/print_bulk", {params: par});
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
                return $http.get('http://127.0.0.1:8000/api/invoice_canon/' + id + '/items/', {params: par}).then(function(resp) {
                    return resp.data;
                });
            }
        }
})

.factory('waybillitems', function($http) {
        return {
            all: function(id) {
                return $http.get('http://127.0.0.1:8000/api/waybill/' + id + '/items/').then(function(resp) {
                    return resp.data.items;
                });
            }
        };
    });