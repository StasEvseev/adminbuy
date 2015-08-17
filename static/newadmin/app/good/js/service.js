/**
 * Created by user on 14.08.15.
 */

angular.module('good.service', ['core.service'])
.factory('goods', function(BaseModelService) {

    var url = 'api/good',
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
    return child;
});
