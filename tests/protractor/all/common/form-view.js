/**
 * Created by user on 14.10.15.
 */
var brow = require('./browser');

var obj = {
    selectItemToMultiselectField: function(el, item) {
        /*
        * Функция выбора записи в мультиселекте.
        * */
        item += 3;
        var deferred = protractor.promise.defer();
        el.click().then(function() {
            brow.waitUntilReady(el.element(by.css("div > div > ul > li")));
            el.element(by.css("li.ui-select-choices-group > div.ui-select-choices-row:nth-child("+item+")")).click().then(function () {
                deferred.fulfill();
            })
        });

        return deferred.promise;
    },

    fillDictSelectField: function(model, value) {
        /*
        * Выбрать значение в dictSelectField.
        * */
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
    }
};


module.exports = obj;