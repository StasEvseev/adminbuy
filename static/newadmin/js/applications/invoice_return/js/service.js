angular.module('invoice_return.service', ['core.service'])

.factory('InvoiceReturnService', function(BaseDictService, invoices) {

    var child = Object.create(BaseDictService);
    child.records = function (text) {
        return invoices.filter(text);
    };

    return child;
})


.factory('invoices_return', function(BaseModelService, $http, apiConfig) {
    var path = apiConfig.baseUrl + '/refund';

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
        return $http.get(apiConfig.baseUrl + "/refund/" + id + "/items").then(function(resp) {
            return resp.data.items;
        });
    };

    child.saveAmountFromInvoice = function (id, items) {
        return $http.put(apiConfig.baseUrl + "/refund/" + id + "/items", {data: {items: items}}).then(function(resp) {
            return resp;
        });
    };

    return child;
});