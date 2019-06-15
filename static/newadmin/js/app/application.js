angular.module('application', [])

.factory("Application", function() {
    return {
        version: function() {
            return "1.1";
        },
        authorLink: function() {
            return "<a target='_blank' href='http://evfam.com'>Evseev Stanislav</a>.";
        }
    }
});