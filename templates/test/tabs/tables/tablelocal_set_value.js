{% if hidden %}
    if(!($scope.{{ hidden|safe }})) {
{% endif %}

    {{modal_ctrl}}RES_GETALL.meth({inner_id: $routeParams.id}, function(data){
        ITEMS{{tab_id}} = data.items;
        $scope.items.{{ tab_id }}ITEMS = ITEMS{{tab_id}};
    });
{% if hidden %}
    }
{% endif %}
