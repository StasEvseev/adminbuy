angular.module('user', [])

.service("User", function($q, $http, apiConfig) {
    var name = "", iconUrl = "", position = "", is_superuser = false, id = '';

    return {
        id: function() {
            return id;
        },
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
            return $http.get(apiConfig.baseUrl + '/profile').then(function(resp) {
                name = resp.data.name;
                iconUrl = resp.data.iconUrl;
                position = resp.data.position;
                is_superuser = resp.data.is_superuser;
                id = resp.data.id;
            }, function(resp) {
                id: '';
                name = '';
                iconUrl = '';
                position = '';
                is_superuser = '';
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