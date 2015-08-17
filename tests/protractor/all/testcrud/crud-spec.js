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

                });

            });
        });

    })
});