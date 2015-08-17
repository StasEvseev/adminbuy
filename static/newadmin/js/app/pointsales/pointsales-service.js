/**
 * Created by user on 27.07.15.
 */

angular.module('pointsales.service', ['core.service'])

.factory('pointsales', function(BaseModelService) {
    var path = 'api/pointsale';

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
});