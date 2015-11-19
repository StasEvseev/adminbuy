{% extends "test/tabs/tables/table-ms-edt/table-ms-atj.js" %}

{% block load %}
    {{modal_ctrl}}RES_GETALL.meth({inner_id: $routeParams.id}, function(data){
        ITEMS{{tab_id}} = data.items;
        $scope.items.{{ tab_id }}ITEMS = ITEMS{{tab_id}};
    });
{% endblock %}