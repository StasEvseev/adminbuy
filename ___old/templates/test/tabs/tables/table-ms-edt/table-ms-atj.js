var ITEMS{{tab_id}} = [];
{% block load %}

{% endblock %}
$scope.items.{{ tab_id }}ITEMS = ITEMS{{tab_id}};

$scope.{{ tab_id }}deleteItem = function(item, event) {
    event.stopPropagation();
    bootbox.confirm("Вы уверены, что хотите удалить запись?", function(result) {
        if (result) {
            var index = ITEMS{{tab_id}}.indexOf(item);
            ITEMS{{tab_id}}.splice(index, 1);
            $scope.items.{{ tab_id }}ITEMS = ITEMS{{tab_id}};
            $scope.$digest();
        }
    });
};

{% for _import in imports %}
    {{ _import.render_to_parent_controller()|safe }}
{% endfor %}