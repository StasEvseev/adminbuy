/**
 * Created by user on 24.08.15.
 */

angular.module('invoice.service', ['core.service'])

.factory('InvoiceService', function(BaseDictService, invoices) {

    var child = Object.create(BaseDictService);
    child.records = function (text) {
        return invoices.filter(text);
    };

//    child.formInclude = function() {
//        return "ReceiverForm";
//    };

//    child.title = function() {
//        return "Создание оптовика";
//    };
//
//    child.titleEdit = function() {
//        return "Редактирование оптовика";
//    };

//    child.resolveEdit = function(item) {
//        return {
//            item: function() {
//                return receivers.getById(item.id);
//            }
//        };
//    };

    return child;
})


.factory('invoices', function(BaseModelService) {
    var path = 'api/invoice_canon';

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