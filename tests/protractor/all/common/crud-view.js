/**
 * Created by user on 14.10.15.
 */
var obj = {
    buttonCreate: function() {
        return $('button.btn-crt').click();
    },
    buttonSave: function() {
        return $("button.btn-sv").click();
    },
    buttonEdit: function() {
        return $("button.btn-edt").click();
    },
    countRows: function() {
        return $("table.dataTable").all(by.css('tbody > tr')).count();
    },
    getRow: function(index) {
        return $("table.dataTable").all(by.css('tbody > tr')).get(index);
    },
    removeRowFalse: function() {
        var deferred = protractor.promise.defer();
        $("div.btn-group").click().then(function() {
            $("a.btn-del").click().then(function() {
                var alertDialog = browser.switchTo().alert();
                alertDialog.dismiss();
                deferred.fulfill();
            });
        });

        return deferred.promise;
    },
    removeRow: function() {
        var deferred = protractor.promise.defer();
        $("div.btn-group").click().then(function() {
            $("a.btn-del").click().then(function() {
                var alertDialog = browser.switchTo().alert();
                alertDialog.accept();
                deferred.fulfill();
            });
        });

        return deferred.promise;
    }
};

module.exports = obj;