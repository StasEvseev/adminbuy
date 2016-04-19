var hlp = require('../common/helper');
var auth = require('../common/auth');
var crud_view = require('../common/crud-view');
var form_view = require('../common/form-view');

beforeEach(function() {
    browser.get('http://localhost:5674');
});

describe('project home page', function() {

    it("authenticate to admin", function() {
        auth.auth('admin', 'admin').then(function() {

            expect(browser.getLocationAbsUrl()).toEqual("/");

        });
    });

    it("correct add role `user to admin", function() {
        hlp.addRoleToRow(0, 'user');

        auth.logout().then(function() {
            auth.auth('admin', 'admin');
        });
    });

    it("add new user", function() {
        hlp.openUserItemAndCreate().then(function() {
            expect(browser.getLocationAbsUrl()).toEqual("/user/create");
            element(by.model("model.login")).sendKeys("Логин");
            element(by.model("model.first_name")).sendKeys("Фамилия");
            element(by.model("model.last_name")).sendKeys("Имя");
            element(by.model("model.email")).sendKeys("a@a.ru");
            element(by.model("model.password")).sendKeys("123");
            element(by.model("model.retypepassword")).sendKeys("123");

            var element_role = element(by.model("model.roles"));
            form_view.selectItemToMultiselectField(element_role, 3).then(function() {
                crud_view.buttonSave().then(function() {
                    hlp.openUserItem().then(function() {
                        crud_view.countRows().then(function(count) {
                            expect(count).toEqual(2);

                            crud_view.getRow(0).click().then(function() {
                                expect(browser.getLocationAbsUrl()).toEqual("/user/2");

                                crud_view.buttonEdit().then(function() {
                                    expect(browser.getLocationAbsUrl()).toEqual("/user/2/edit");

                                    element(by.model("model.login")).sendKeys("Логин2");
                                    element(by.model("model.first_name")).sendKeys("Фамилия2");
                                    element(by.model("model.last_name")).sendKeys("Имя2");
                                    element(by.model("model.email")).sendKeys("a@a2.ru");

                                    crud_view.buttonSave().then(function() {
                                        expect(browser.getLocationAbsUrl()).toEqual("/user/2");

                                        hlp.openUserItem().then(function() {
                                            crud_view.countRows().then(function (count) {
                                                expect(count).toEqual(2);
                                            });

                                            crud_view.getRow(0).click().then(function() {
                                                crud_view.removeRow().then(function() {

                                                    hlp.openUserItem().then(function() {
                                                        crud_view.countRows().then(function(count) {
                                                            expect(count).toEqual(1);
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
        })
    });

//    it("CRUD receiver", function() {
//        hlp.CRUDSimple("receiver-item", "/receiver", function() {
//            element(by.model("model.fname")).sendKeys("Фамилия");
//            element(by.model("model.lname")).sendKeys("Имя");
//            element(by.model("model.pname")).sendKeys("Отчество");
//            element(by.model("model.address")).sendKeys("Адрес");
//            element(by.model("model.passport")).sendKeys("1234523123");
//        },
//        function() {
//            element(by.model("model.fname")).sendKeys("Фамилия2");
//            element(by.model("model.lname")).sendKeys("Имя2");
//            element(by.model("model.pname")).sendKeys("Отчество2");
//            element(by.model("model.address")).sendKeys("Адрес2");
//            element(by.model("model.passport")).clear();
//            element(by.model("model.passport")).sendKeys("1111222222");
//        });
//    });
//
//    it("CRUD commodity", function() {
//        var urlclass = hlp.urlclassCommodity();
//        hlp.CRUDSimple(urlclass[0], urlclass[1], function() {
//            hlp.fillFormCommodity("Название", "Тематика", true);
//        }, function() {
//            hlp.fillFormCommodity("Название2", "Тематика2", true);
//        });
//    });
//
//    it("CRUD pointsale", function() {
//        var name = "Название",
//            address = "Адрес",
//            is_central = false,
//            name2 = "Название2",
//            address2 = "Адрес2",
//            is_central2 = true;
//        var urlclass = hlp.urlclassPointsale();
//        hlp.CRUDSimple(urlclass[0], urlclass[1], function() {
//            hlp.fillFormPointsale(name, address, is_central);
//        }, function() {
//            hlp.fillFormPointsale(name2, address2, is_central2);
//        });
//    });
//
//    it("CRUD good", function() {
//        var name_commodity = "Название",
//            thematic_commodity = "Тематика",
//            name_commodity2 = "Другое",
//            thematic_commodity2 = "Другая";
//        hlp.createCommodity(name_commodity, thematic_commodity, true).then(function() {
//            hlp.createCommodity(name_commodity2, thematic_commodity2, true)
//        }).then(function() {
//            hlp.CRUDSimple("good-item", "/good", function() {
//
//                form_view.fillDictSelectField("model.commodity", name_commodity).then(function() {
//                    element(by.model("model.number_local")).sendKeys("1");
//                    element(by.model("model.number_global")).sendKeys("1");
//                    element(by.model("model['price.price_retail']")).sendKeys("1.2");
//                    element(by.model("model['price.price_gross']")).sendKeys("1.4");
//                });
//            }, function() {
//                form_view.fillDictSelectField("model.commodity", name_commodity2).then(function() {
//                    element(by.model("model.number_local")).sendKeys("2");
//                    element(by.model("model.number_global")).sendKeys("2");
//                    element(by.model("model['price.price_retail']")).sendKeys("2");
//                    element(by.model("model['price.price_gross']")).sendKeys("4");
//                });
//            });
//        });
//    });
});