angular.module('invoice.service', ['core.service'])

.factory('InvoiceService', function(BaseDictService, invoices) {

    var child = Object.create(BaseDictService);
    child.records = function (text) {
        return invoices.filter(text);
    };

    return child;
})
.factory('InvoiceServiceAddNew', function(BaseDictService, invoices) {

    var child = Object.create(BaseDictService);
    child.records = function (text) {
        return invoices.filter(text, 1, 50, {add_from_invoice: true, number: text, date: text});
    };

    return child;
})


.factory('invoices', function(BaseModelService, $http, apiConfig) {
    var path = apiConfig.baseUrl + '/invoice_canon';

    var child = Object.create(BaseModelService);
    child._getPath = function () {
        return path;
    };

    child.filter = function(text, page, count, extra_params) {
        return BaseModelService.filter.call(this, text, page, count, extra_params).then(function(resp) {
            return resp.data.items;
        });
    };

    child.getItems = function(id) {
        return $http.get(apiConfig.baseUrl + "/invoice_canon/" + id + "/items").then(function(resp) {
            return resp.data.items;
        });
    };

    child.getRowInvoiceIn = function(id) {
        return $http.get(apiConfig.baseUrl + "/invoiceprice2items/" + id).then(function(resp) {
            return resp.data.items;
        });
    };

    child.savePriceFromInvoice = function(id, items) {
        return $http.post(apiConfig.baseUrl + "/pricebulkinvoice", {data: {invoice_id: id, items: items}}).then(function(resp) {
            return resp;
        });
    };

    return child;
});