describe('project home page', function() {

    beforeEach(function() {
        browser.get('http://localhost:5674');
    });

//    it('should be authorization', function() {
////        browser.get('http://localhost:5674');
//
//
//    });
    it("should be create user", function() {

        var login = element(by.model('login')),
            password = element(by.model('password')),
            btn_submit = element(by.css("button.btn"));
        login.sendKeys("admin");
        password.sendKeys("admin");
        btn_submit.click().then(function() {
              expect(browser.getLocationAbsUrl()).toEqual("/");
        });

        var liitem = $("ul.sidebar-menu > li.user-menu");
        var anchor = liitem.element(by.css("ul > li > a.user-item"));
        liitem.element(by.tagName("a")).click().then(function() {
            anchor.click().then(function() {
                expect(browser.getLocationAbsUrl()).toEqual("/user");
                $('button.btn-crt').click().then(function() {
                    expect(browser.getLocationAbsUrl()).toEqual("/user/create");
                    element(by.model("model.login")).sendKeys("Логин");
                    element(by.model("model.first_name")).sendKeys("Фамилия");
                    element(by.model("model.last_name")).sendKeys("Имя");
                    element(by.model("model.email")).sendKeys("a@a.ru");
                    element(by.model("model.password")).sendKeys("123");
                    element(by.model("model.retypepassword")).sendKeys("123");

                    $("button.btn-sv").click().then(function() {
                        anchor.click().then(function() {
                            $("table.dataTable").all(by.css('tbody > tr')).count().then(function(count) {
                                expect(count).toEqual(2);

                                $("table.dataTable").all(by.css('tbody > tr')).get(0).click().then(function() {
                                    expect(browser.getLocationAbsUrl()).toEqual("/user/2");

                                    $("button.btn-edt").click().then(function() {
                                        expect(browser.getLocationAbsUrl()).toEqual("/user/2/edit");

                                        element(by.model("model.login")).sendKeys("Логин2");
                                        element(by.model("model.first_name")).sendKeys("Фамилия2");
                                        element(by.model("model.last_name")).sendKeys("Имя2");
                                        element(by.model("model.email")).sendKeys("a@a2.ru");

                                        $("button.btn-sv").click().then(function() {
                                            expect(browser.getLocationAbsUrl()).toEqual("/user/2");
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