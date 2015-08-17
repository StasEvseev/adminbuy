describe('project home page', function() {

    beforeEach(function() {
        browser.get('http://localhost:5674');
    });

    it('should be authorization', function() {
//        browser.get('http://localhost:5674');

        var login = element(by.model('login')),
            password = element(by.model('password')),
            btn_submit = element(by.css("button.btn"));
        login.sendKeys("admin");
        password.sendKeys("admin");
        btn_submit.click().then(function() {
              expect(browser.getLocationAbsUrl()).toEqual("/");
        });
    });
    it("should be create user", function() {
        var countItems;
        var liitem = $("ul.sidebar-menu > li.user-menu");
        var table;
        liitem.element(by.tagName("a")).click().then(function() {
            liitem.element(by.css("ul > li > a.user-item")).click().then(function() {
                expect(browser.getLocationAbsUrl()).toEqual("/user");
                countItems = $("table.dataTable > tbody > tr").length;
                $('button.btn-crt').click().then(function() {
                    expect(browser.getLocationAbsUrl()).toEqual("/user/create");
                    element(by.model("model.login")).sendKeys("Логин");
                    element(by.model("model.first_name")).sendKeys("Фамилия");
                    element(by.model("model.last_name")).sendKeys("Имя");
                    element(by.model("model.email")).sendKeys("a@a.ru");
                    element(by.model("model.password")).sendKeys("123");
                    element(by.model("model.retypepassword")).sendKeys("123");

                    $("button.btn-sv").click().then(function() {
                        liitem.element(by.css("ul > li > a.user-item")).click().then(function() {
                            browser.pause()
                            expect($("table.dataTable > tbody > tr").length).toEqual(2);

                            $("table.dataTable > tbody > tr")[0].click().then(function() {
                                expect(browser.getLocationAbsUrl()).toEqual("/user/2");
                            });
                        });
                    });
                });

            });
        });

    })
});