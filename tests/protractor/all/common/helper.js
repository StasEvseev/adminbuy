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
    },

    fillDictSelectField: function(model, value) {
        var q = protractor.promise.defer();
        var comm_field = element(by.model(model)),
            comm_input = comm_field.element(by.css("div > div > input")),
            comm_list = comm_field.element(by.css("div > div > ul > li"));
        comm_field.element(by.css("div > div")).click().then(function() {
            comm_input.sendKeys(value);
            browser.driver.wait(function(){
                return comm_list.all(by.css("div.ui-select-choices-row")).count().then(function(count){
                    return 0 < count;
                });
            }, 2000);
            comm_list.all(by.css("div.ui-select-choices-row")).first().click().then(function() {
                q.fulfill();
            });
        });

        return q.promise;
    },

    urlclassPointsale: function() {
        return ["pointsale-item", "/pointsale"];
    },
    fillFormPointsale: function(name, address, is_central) {

        element(by.model("model.name")).sendKeys(name);
        element(by.model("model.address")).sendKeys(address);

        if (is_central) {
            if (!element(by.model('model.is_central')).isSelected()) {
                element(by.model("model.is_central")).click();
            }
        } else {
            if(element(by.model('model.is_central')).isSelected()) {
                element(by.model("model.is_central")).click();
            }
        }
    },

    urlclassCommodity: function() {
        return ["commodity-item", "/commodity"];
    },
    fillFormCommodity: function(name, thematic, is_num) {
        element(by.model("model.name")).sendKeys(name);
        element(by.model("model.thematic")).sendKeys(thematic);
        if (is_num) {
            if (!element(by.model('model.numeric')).isSelected()) {
                element(by.model("model.numeric")).click();
            }
        } else {
            if(element(by.model('model.numeric')).isSelected()) {
                element(by.model("model.numeric")).click();
            }
        }
    }
};

obj['createPointsale'] = function(name, address, is_central) {
    var q = protractor.promise.defer();
    var urlclass = obj.urlclassPointsale();
    var anchor = $("ul.sidebar-menu > li > a." + urlclass[0]);
    anchor.click().then(function() {
        obj.buttonCreate().then(function() {
            obj.fillFormPointsale(name, address, is_central);
            obj.buttonSave().then(function() {
                anchor.click().then(function() {
                    q.fulfill();
                });
            });
        })
    });
    return q.promise;
};

obj['createCommodity'] = function(name, thematic, is_num) {
    var q = protractor.promise.defer();
    var urlclass = obj.urlclassCommodity();
    var anchor = $("ul.sidebar-menu > li > a." + urlclass[0]);
    anchor.click().then(function() {
        obj.buttonCreate().then(function() {
            obj.fillFormCommodity(name, thematic, is_num);
            obj.buttonSave().then(function() {
                anchor.click().then(function() {
                    q.fulfill();
                });
            });
        })
    });
    return q.promise;
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