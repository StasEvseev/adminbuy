
debugger
app.controller('{{ modal_cntr }}', function($scope, object, $modalInstance, {{ modal_cntr }}RES_UPDATE, {{ modal_cntr }}RES_CREATE) {
    var isNew = true;
    $scope.model = {};
    $scope.errors = {};
    $scope.validate = {};

    console.log(object);

    if(object) {
        isNew = false;
        $scope.model = object;
    }
    $scope.isNew = isNew;

    var setError = function(attr, message) {
        if (message) {
            $scope.errors[attr] = true;
        } else {
            $scope.errors[attr] = false;
        }
    };

    $scope.ok = function () {
//        if(!$scope.model.name) {
//            setError("name", "Поле наименование не должно быть пустым");
//            $scope.model.validate.message = "Поле наименование не должно быть пустым";
//        } else {
//            setError("name");
//            $scope.model.validate.message = undefined;
//        }
//        if (_.indexOf(_.values($scope.model.errors), true) != -1) {
//            return;
//        }

        if(isNew) {
            {{ modal_cntr }}RES_CREATE.meth({data: {
                {% for fld in form.fields %}
                    '{{ fld.get_form_id()|safe }}': {{ fld.get_form_attr()|safe }},
                {% endfor %}
                }},
                function(data) {
                    $modalInstance.close(data);
                },
                function(data) {
                    console.log(data);
                    setError("name", "Поле наименование должны быть уникальным");
                    $scope.model.validate.message = data.data.message;
                }
            );
        } else {
            {{ modal_cntr }}RES_UPDATE.meth({id: object.id, data: {
                    {% for fld in form.fields %}
                        '{{ fld.get_form_id()|safe }}': {{ fld.get_form_attr()|safe }},
                    {% endfor %}
                }},
                function(data) {
                    $modalInstance.close(data);
                }, function (data) {

                })
        }
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});

app.factory("{{ modal_cntr }}RES_CREATE", function($resource, Base64) {
  return $resource("{{ url_create }}", {}, {
    meth: { method: "PUT", isArray: false , headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("{{ modal_cntr }}RES_GETALL", function($resource, Base64) {
  return $resource("{{ url_getall }}", {}, {
    meth: { method: "GET", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("{{ modal_cntr }}RES_GET", function($resource, Base64) {
  return $resource("{{ url_get }}", {id: "@id"}, {
    meth: { method: "GET", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("{{ modal_cntr }}RES_UPDATE", function($resource, Base64) {
  return $resource("{{ url_update }}", {id: "@id"}, {
    meth: { method: "POST", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
})

.factory("{{ modal_cntr }}RES_DELETE", function($resource, Base64) {
  return $resource("{{ url_delete }}", {id: "@id"}, {
    meth: { method: "DELETE", isArray: false, headers: { Authorization: 'Basic ' + Base64.encode(TOKEN + ':' + 'unused') }}
  });
});