{% extends "test/tabs/tables/tablelocal_add_to_js.js" %}

{% block edit %}
    if(!$scope.editMode || $scope.model.status == 3) {
        return;
    }
{% endblock %}