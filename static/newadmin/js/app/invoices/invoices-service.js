/**
 * Created by user on 03.07.15.
 */

angular.module('invoices.service', ['core.service'])

.factory('invoices', function(BaseModelService) {
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

    return child;
})

.factory('invoicesitems', function($http) {
        var path = 'api/waybill/:id/items';

        return {
            all: function(id) {
                return $http.get('api/waybill/' + id + '/items').then(function(resp) {
                    return resp.data.items;
                });
            }
        };
    });