describe('project home page', function() {
  it('should be authorization', function() {
    browser.get('http://localhost:5674');
    expect(browser.getLocationAbsUrl()).toEqual("/signin");
    expect(browser.getTitle()).toEqual('Газеты ЖУРНАЛЫ | Dashboard');

    var goButton = element(by.css('div.login-logo'));
    goButton.click();
    expect(browser.getLocationAbsUrl()).toEqual("/signin");

    ["mailbox", "invoice_in", "pointsale", "receiver", "user", "commodity", "good"].forEach(function(item) {
        browser.get("http://localhost:5674/admin2#/" + item);
        expect(browser.getLocationAbsUrl()).toEqual("/signin");
    });
  });
});