/**
 * Created by user on 28.07.15.
 */

angular.module('receivers.service', ['core.service'])
.factory('receivers', function(BaseModelService) {

    var url = '/api/receiver',
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
