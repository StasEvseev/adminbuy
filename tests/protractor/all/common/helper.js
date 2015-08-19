var obj = {
    authAdmin: function() {
        var login = element(by.model('login')),
            password = element(by.model('password')),
            btn_submit = element(by.css("button.btn"));
        login.sendKeys("admin");
        password.sendKeys("admin");
        return btn_submit.click();
    },
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

obj['CRUDSimple'] = function(aclass, url, function_create, function_edit) {
    var anchor = $("ul.sidebar-menu > li > a." + aclass);
    anchor.click().then(function() {
        expect(browser.getLocationAbsUrl()).toEqual(url);
        obj.buttonCreate().then(function() {
            expect(browser.getLocationAbsUrl()).toEqual(url + "/create");

            function_create();

            obj.buttonSave().then(function() {
                anchor.click().then(function() {
                    obj.countRows().then(function(count) {
                        expect(count).toEqual(1);

                        obj.getRow(0).click().then(function() {
                            expect(browser.getLocationAbsUrl()).toEqual(url + "/1");

                            obj.buttonEdit().then(function() {
                                expect(browser.getLocationAbsUrl()).toEqual(url + "/1/edit");

                                function_edit();

                                obj.buttonSave().then(function() {
                                    expect(browser.getLocationAbsUrl()).toEqual(url + "/1");

                                    anchor.click().then(function() {
                                        obj.countRows().then(function (count) {
                                            expect(count).toEqual(1);
                                        });
                                        obj.getRow(0).click().then(function() {
                                            obj.removeRowFalse().then(function() {
                                                anchor.click().then(function() {
                                                    obj.countRows().then(function(count) {
                                                        expect(count).toEqual(1);
                                                        obj.getRow(0).click().then(function() {
                                                            obj.removeRow().then(function() {
                                                                obj.countRows().then(function(count) {
                                                                    expect(count).toEqual(0);
                                                                });
                                                            });
                                                        });
                                                    });
                                                });
                                            });
                                        });
                                    });
                                });
                            });
                        });
                    });
                });
            });
        });
    });
};

module.exports = obj;