/**
 * Created by Stanislav on 26.11.2015.
 */

angular.module('{{ name }}.service', ['core.service'])
.factory('{{ name_service }}', function(BaseModelService) {

    var url = 'api/{{ name }}',
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
