//var helper = require('../common/helper');
var form_view = require('./form-view');
var crud_view = require('./crud-view');

var obj = {
    mapRole: function() {
        return {
            'admin': 'div#ui-select-choices-row-0-0',
            'driver': 'div#ui-select-choices-row-0-1',
            'vendor': 'div#ui-select-choices-row-0-2',
            'user': 'div#ui-select-choices-row-0-3'
        }
    },

    mapRoleIndex: function() {
        return {
            'admin': 0,
            'driver': 1,
            'vendor': 2,
            'user': 3
        }
    },

    addRoleToRow: function(row, role) {
        var deferred = protractor.promise.defer();
        var self = this;
        self.openUserItem().then(function() {
            crud_view.getRow(row).click().then(function() {
                crud_view.buttonEdit().then(function() {

                    form_view.selectItemToMultiselectField(
                        element(by.model("model.roles")),
                        self.mapRoleIndex()[role]
                    ).then(function() {
                        crud_view.buttonSave().then(function() {
                            deferred.fulfill();
                        })
                    });
                });
            });
        });
        return deferred.promise;
    },

    openUserItem: function() {
        /*
        * Открываем пункт `Пользователи`
        * */
        var deferred = protractor.promise.defer();
        var liitem = $("ul.sidebar-menu > li.user-menu");
        var anchor = liitem.element(by.css("ul > li > a.user-item"));
        liitem.element(by.tagName("a")).click().then(function() {
            anchor.click().then(function () {
                expect(browser.getLocationAbsUrl()).toEqual("/user");

                deferred.fulfill();
            })
        });

        return deferred.promise;
    },

    openUserItemAndCreate: function() {
        var deferred = protractor.promise.defer();

        this.openUserItem().then(function() {
            crud_view.buttonCreate().then(function() {
                deferred.fulfill();
            })
        });

        return deferred.promise;
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