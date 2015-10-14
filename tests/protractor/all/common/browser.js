/**
 * Created by user on 14.10.15.
 */


var obj = {
    waitUntilReady: function (elm) {
        browser.wait(function () {
            return elm.isPresent();
        },10000);
        browser.wait(function () {
            return elm.isDisplayed();
        },10000);
    }
};

module.exports = obj;