app.controller('{{ modal_cntr }}', function($scope, $rootScope, object, $modalInstance,{{ modal_cntr }}RES_UPDATE, {{ modal_cntr }}RES_CREATE
{% for modal in modals %}
    ,{{ modal.depend_js_getall()|safe }}
    {% endfor %}
{% for table in form.form_tables %}
        ,{{ table.depend_js()|safe }}
    {% endfor %}) {
    var isNew = true;
    $scope.model = {};
    $scope.errors = {};
    $scope.validate = {};

    {% for table in form.form_tables %}
        {{ table.render_js()|safe }}
    {% endfor %}

    {% for modal in modals %}
        {{ modal.add_to_js()|safe }}
    {% endfor %}

    console.log(object);

    if(object) {
        isNew = false;
        $scope.model = _.clone(object);
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
        $modalInstance.close($scope.model);
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


    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});