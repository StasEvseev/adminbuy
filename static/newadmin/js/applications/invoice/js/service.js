/**
 * Created by user on 24.08.15.
 */

angular.module('invoice.service', ['core.service'])

.factory('InvoiceService', function(BaseDictService, invoices) {

    var child = Object.create(BaseDictService);
    child.records = function (text) {
        return invoices.filter(text);
    };

    return child;
})


.factory('invoices', function(BaseModelService, $http) {
    var path = 'http://127.0.0.1:8000/api/invoice_canon/';

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
        return $http.get("http://127.0.0.1:8000/api/invoice_canon/" + id + "/items").then(function(resp) {
            return resp.data.items;
        });
    };

    child.getRowInvoiceIn = function(id) {
        return $http.get("http://127.0.0.1:8000/api/invoiceprice2items/" + id).then(function(resp) {
            return resp.data.items;
        });
    };

    child.savePriceFromInvoice = function(id, items) {
        return $http.post("http://127.0.0.1:8000/api/pricebulkinvoice/", {data: {invoice_id: id, items: items}}).then(function(resp) {
            return resp;
        });
    };

    return child;
});