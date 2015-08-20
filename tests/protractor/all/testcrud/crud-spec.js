var hlp = require('../common/helper');

beforeEach(function() {
    browser.get('http://localhost:5674');
});

describe('project home page', function() {
    it("should be create user", function() {
        hlp.authAdmin().then(function() {
              expect(browser.getLocationAbsUrl()).toEqual("/");
        });

        var liitem = $("ul.sidebar-menu > li.user-menu");
        var anchor = liitem.element(by.css("ul > li > a.user-item"));
        liitem.element(by.tagName("a")).click().then(function() {
            anchor.click().then(function() {
                expect(browser.getLocationAbsUrl()).toEqual("/user");
                hlp.buttonCreate().then(function() {
                    expect(browser.getLocationAbsUrl()).toEqual("/user/create");
                    element(by.model("model.login")).sendKeys("Логин");
                    element(by.model("model.first_name")).sendKeys("Фамилия");
                    element(by.model("model.last_name")).sendKeys("Имя");
                    element(by.model("model.email")).sendKeys("a@a.ru");
                    element(by.model("model.password")).sendKeys("123");
                    element(by.model("model.retypepassword")).sendKeys("123");

                    hlp.buttonSave().then(function() {
                        anchor.click().then(function() {
                            hlp.countRows().then(function(count) {
                                expect(count).toEqual(2);

                                hlp.getRow(0).click().then(function() {
                                    expect(browser.getLocationAbsUrl()).toEqual("/user/2");

                                    hlp.buttonEdit().then(function() {
                                        expect(browser.getLocationAbsUrl()).toEqual("/user/2/edit");

                                        element(by.model("model.login")).sendKeys("Логин2");
                                        element(by.model("model.first_name")).sendKeys("Фамилия2");
                                        element(by.model("model.last_name")).sendKeys("Имя2");
                                        element(by.model("model.email")).sendKeys("a@a2.ru");

                                        hlp.buttonSave().then(function() {
                                            expect(browser.getLocationAbsUrl()).toEqual("/user/2");

                                            anchor.click().then(function() {
                                                hlp.countRows().then(function (count) {
                                                    expect(count).toEqual(2);
                                                });

                                                hlp.getRow(0).click().then(function() {
                                                    hlp.removeRow().then(function() {
                                                        hlp.countRows().then(function(count) {
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
        });
    });

    it("CRUD receiver", function() {
        hlp.CRUDSimple("receiver-item", "/receiver", function() {
            element(by.model("model.fname")).sendKeys("Фамилия");
            element(by.model("model.lname")).sendKeys("Имя");
            element(by.model("model.pname")).sendKeys("Отчество");
            element(by.model("model.address")).sendKeys("Адрес");
            element(by.model("model.passport")).sendKeys("1234523123");
        },
        function() {
            element(by.model("model.fname")).sendKeys("Фамилия2");
            element(by.model("model.lname")).sendKeys("Имя2");
            element(by.model("model.pname")).sendKeys("Отчество2");
            element(by.model("model.address")).sendKeys("Адрес2");
            element(by.model("model.passport")).clear();
            element(by.model("model.passport")).sendKeys("1111222222");
        });
    });

    it("CRUD commodity", function() {
        var urlclass = hlp.urlclassCommodity();
        hlp.CRUDSimple(urlclass[0], urlclass[1], function() {
            hlp.fillFormCommodity("Название", "Тематика", true);
        }, function() {
            hlp.fillFormCommodity("Название2", "Тематика2", true);
        });
    });

    it("CRUD pointsale", function() {
        hlp.CRUDSimple("pointsale-item", "/pointsale", function() {
            element(by.model("model.name")).sendKeys("Название");
            element(by.model("model.address")).sendKeys("Адрес");
            element(by.model("model.is_central")).click();
        }, function() {
            element(by.model("model.name")).sendKeys("Название2");
            element(by.model("model.address")).sendKeys("Адрес2");
            element(by.model("model.is_central")).click();
        });
    });

    it("CRUD good", function() {
        var name_commodity = "Название",
            thematic_commodity = "Тематика",
            name_commodity2 = "Название2",
            thematic_commodity2 = "Тематика2";
        hlp.createCommodity(name_commodity, thematic_commodity, true).then(function() {
            hlp.createCommodity(name_commodity2, thematic_commodity2, true)
        }).then(function() {
            hlp.CRUDSimple("good-item", "/good", function() {

                hlp.fillDictSelectField("model.commodity", name_commodity).then(function() {
                    element(by.model("model.number_local")).sendKeys("1");
                    element(by.model("model.number_local")).sendKeys("1");
                    element(by.model("model.number_global")).sendKeys("1");
                    element(by.model("model['price.price_retail']")).sendKeys("1.2");
                    element(by.model("model['price.price_gross']")).sendKeys("1.4");
                });
            }, function() {
                hlp.fillDictSelectField("model.commodity", name_commodity).then(function() {
                    element(by.model("model.number_local")).sendKeys("2");
                    element(by.model("model.number_global")).sendKeys("2");
                    element(by.model("model.price.price_retail")).sendKeys("2");
                    element(by.model("model.price.price_gross")).sendKeys("4");
                });
            });
        });
    });
});