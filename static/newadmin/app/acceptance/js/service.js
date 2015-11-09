/**
 * Created by user on 24.08.15.
 */

angular.module('acceptance.service', ['core.service'])

.factory('AcceptanceService', function(BaseDictService, acceptances) {

    var child = Object.create(BaseDictService);
    child.records = function (text) {
        return acceptances.filter(text);
    };

    return child;
})


.factory('acceptances', function(BaseModelService, $http) {
    var path = 'api/acceptance';

    var child = Object.create(BaseModelService);
    child._getPath = function () {
        return path;
    };

    child.filter = function(text, page, count) {
        return BaseModelService.filter.call(this, text, page, count).then(function(resp) {
            return resp.data.items;
        });
    };

    child.getItems = function(id) {
        return $http.get("/api/acceptance/" + id + "/items").then(function(resp) {
            return resp.data.items;
        });
    };

//    child.getRowInvoiceIn = function(id) {
//        return $http.get("/api/invoiceprice2items/" + id).then(function(resp) {
//            return resp.data.items;
//        });
//    };

//    child.savePriceFromInvoice = function(id, items) {
//        return $http.post("/api/pricebulkinvoice", {data: {invoice_id: id, items: items}}).then(function(resp) {
//            return resp;
//        });
//    };

    return child;
});