/**
 * Created by user on 24.08.15.
 */

angular.module("utils", [])
.factory("arrayhelp", function() {
    return {
        getElemsByIds: function(items_ids, items) {
            return _.map(items_ids,
                function(it) {
                    var index = _.findIndex(items, function(item) {return item.id == it});
                    return items[index];
                }
            );
        }
    }
});
