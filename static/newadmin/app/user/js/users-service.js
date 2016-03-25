/**
 * Created by user on 12.08.15.
 */

angular.module('users.service', ['core.service'])

.factory('RoleService', function(BaseDictService, $q, roles) {

    var child = Object.create(BaseDictService);
        var items;
    child.records = function (text) {
        return roles.filter(text);
    };

    return child;
})


.factory('roles', function(BaseModelService) {
        var url = '/api/role';

        var child = Object.create(BaseModelService);
        child._getPath = function () {
            return url;
        };
        child.filter = function(text, page, count) {
            return BaseModelService.filter.call(this, text, page, count).then(function(resp) {
                return resp.data.items;
            });
        };
        return child;
    })

.factory('users', function(BaseModelService) {

    var url = '/api/user',
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
