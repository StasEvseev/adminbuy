/**
 * Created by user on 14.08.15.
 */

angular.module('collects.service', ['core.service'])
.factory('collects', function(BaseModelService, $http) {

    var url = '/api/collect',
        items;

    var child = Object.create(BaseModelService);
    child._getPath = function () {
        return url;
    };
    child.filter = function(text, page, count) {
        return BaseModelService.filter.call(this, text, page, count).then(function(resp) {
            items = resp.data.items;
            return items;
        });
    };

//    child.printBarCode = function(good_id) {
//        return $http.get("/api/good/" + good_id + "/printbarcode");
//    };
    return child;
});
