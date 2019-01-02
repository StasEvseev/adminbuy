/**
 * Created by user on 27.07.15.
 */

angular.module('pointsales.service', ['core.service'])

.factory('pointsalesgoods', function($http, BaseModelService){
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
        return "http://127.0.0.1:8000/api/pointsale/" + pointId + "/items";
    };
    return child;
})

.factory('pointsales', function($http, BaseModelService) {
    var path = 'http://127.0.0.1:8000/api/pointsale/';

    var child = Object.create(BaseModelService);
    child._getPath = function () {
        return path;
    };

    child.filter = function(text, page, count) {
        return BaseModelService.filter.call(this, text, page, count).then(function(resp) {
            return resp.data.items;
        });
    };

    child.getCentralPoint = function() {
        return $http.get("http://127.0.0.1:8000/api/pointsale/", {params: {is_central: 'True'}}).then(function(resp) {
            var res = undefined;
            if (resp.data.count) {
                res = resp.data.items[0]
            }
            return res;
        });
    };

    child.getSlavePoint = function() {
        return $http.get("http://127.0.0.1:8000/api/pointsale/", {params: {is_central: 'False'}}).then(function(resp) {
            return resp.data.items;
        });
    };

    return child;
});