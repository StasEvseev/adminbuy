app.controller('{{ modal_cntr }}', function($scope, $rootScope, object, $modalInstance, {{ modal_cntr }}RES_UPDATE, {{ modal_cntr }}RES_CREATE
    {% for modal in modals %}
    ,{{ modal.depend_js_getall()|safe }}
    {% endfor %}) {
    var isNew = true;
    $scope.model = {};
    $scope.errors = {};
    $scope.validate = {};

    {% for modal in modals %}
        {{ modal.add_to_js()|safe }}
    {% endfor %}

    {% for field in form.fields %}
        {{ field.initialize_controller()|safe }}
    {% endfor %}

    console.log(object);

    if(object) {
        isNew = false;
        $scope.model = object;
    }
    $scope.isNew = isNew;

    var setError = function(attr, message) {
        if (message) {
            $scope.errors[attr] = true;
            $scope.validate[attr] = message;
        } else {
            $scope.errors[attr] = false;
            $scope.validate[attr] = message;
        }
    };

    $scope.ok = function () {
        {% for fld in form.fields %}
            {% for val in fld.validators %}
                {{val.validate_js()|safe}}
            {% endfor %}
        {% endfor %}

        if (_.indexOf(_.values($scope.errors), true) != -1) {
            toastr.error(_.filter(_.values($scope.validate), function(item) { if (item == undefined) {return false;} return true;}).join("<br/>"), 'Ошибка валидации!');
            return;
        }

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
                    toastr.error(data.data.message, 'Ошибка сохранения!');
//                    $scope.validate.message = data.data.message;
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
                    toastr.error(data.data.message, 'Ошибка сохранения!');
                })
        }
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});