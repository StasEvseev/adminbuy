/**
 * Created by user on 27.07.15.
 */

angular.module('pointsales.service', ['core.service'])

.factory('pointsalesgoods', function($http, BaseModelService, apiConfig){
//    var path = '';
    var child = Object.create(BaseModelService);
    var pointId;
    child.setPointId = function(id) {
        pointId = id;
    };

    child.filter = function(text, page, count) {
        return BaseModelService.filter.call(this, text, page, count).then(function(resp) {
            return resp.data.items;
        });
    };

    child._getPath = function() {
        return apiConfig.baseUrl + "/pointsale/" + pointId + "/items";
    };
    return child;
})

.factory('pointsales', function($http, BaseModelService, apiConfig) {
    var path = apiConfig.baseUrl + "/pointsale";

    var child = Object.create(BaseModelService);
    child._getPath = function () {
        return path;
    };

    child.filter = function(text, page, count, extra_params) {
        return BaseModelService.filter.call(this, text, page, count, extra_params).then(function(resp) {
            return resp.data.items;
        });
    };

    child.getCentralPoint = function() {
        return $http.get(apiConfig.baseUrl + "/pointsale", {params: {is_central: 'True', active: 'True'}}).then(function(resp) {
            var res = undefined;
            if (resp.data.count) {
                res = resp.data.items[0]
            }
            return res;
        });
    };

    child.getSlavePoint = function() {
        return $http.get(apiConfig.baseUrl + "/pointsale", {params: {is_central: 'False', active: 'True'}}).then(function(resp) {
            return resp.data.items;
        });
    };

    return child;
});