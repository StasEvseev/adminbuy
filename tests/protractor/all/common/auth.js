/**
 * Created by user on 14.10.15.
 */
var brow = require('./browser');

var obj = {
    auth: function(user, password) {
        var deferred = protractor.promise.defer();
        var login = element(by.model('login')),
            password_el = element(by.model('password')),
            btn_submit = element(by.css("button.btn"));
        login.sendKeys(user);
        password_el.sendKeys(password);

        btn_submit.click().then(function() {
            brow.waitUntilReady(element(by.css("div.content-wrapper")));
            deferred.fulfill();
        });

        return deferred.promise;
    },

    logout: function() {
        var deferred = protractor.promise.defer();
        element(by.css("li.user")).click().then(function() {
            element(by.css("a.logout-btn")).click().then(function() {
                brow.waitUntilReady(element(by.css("div.login-page")));
                deferred.fulfill();
            });
        });

        return deferred.promise;
    }
};

module.exports = obj;