/**
 * Created by user on 27.07.15.
 */

angular.module("core.utils", [])

.factory("remoteHelper", function($http) {
        return {
            itemById: function(url, id) {
                url = url.replace(/\/?$/, '/');
                return $http.get(url + id).then(function(resp){
                    return resp.data;
                });
            },
            itemsByIds: function(url, ids) {
                return $http.get(url, {params: {'ids': ids}}).then(function(resp){
                    return resp.data;
                });
            },
            filterItems: function(url, params) {
                var prms = angular.copy(params);

                prms['count'] = params['count'] || 10;
                prms['page'] = params['page'] || 1;

                return $http.get(url, {params: prms});
            },
            createParams: function(text, field, page, count) {
                var params = {};
                if (text) {
                    params['filter_text'] = text;
                    params['filter_field'] = field ? field : 'filter_field';
                }
                params['page'] = page ? page : 1;
                params['count'] = count ? count : 10;
                return params;
            },
            update: function(url, id, params) {
                url = url.replace(/\/?$/, '/');
                return $http.post(url + id, {data: params});
            },
            create: function(url, params) {
                return $http.put(url, {data: params});
            },
            delete_: function(url, id) {
                url = url.replace(/\/?$/, '/');
                return $http.delete(url + id);
            }
        }
    });