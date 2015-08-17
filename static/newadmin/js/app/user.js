angular.module('user', [])

.service("User", function($q, $http) {
    var name = "", iconUrl = "", position = "", is_superuser = false;

    return {
        name: function() {
            return name;
        },
        iconUrl: function() {
            return iconUrl;
        },
        position: function() {
            return position;
        },
        is_superuser: function() {
            return is_superuser;
        },
        fetch: function() {
            return $http.get('/api/profile').then(function(resp) {
                name = resp.data.name;
                iconUrl = resp.data.iconUrl;
                position = resp.data.position;
                is_superuser = resp.data.is_superuser;
            });
        }
    }
})

.factory("Company", function () {
    return {
        nameInvoice: function() {
            return "ИП Евсеева";
        },
        name: function() {
            return "<b>Газеты </b>ЖУРНАЛЫ";
        },
        nameShort: function() {
            return "<b>Г</b>Ж";
        }
    }
});