var ITEMS{{tab_id}} = [];
{% block load %}

{% endblock %}
$scope.items.{{ tab_id }}ITEMS = ITEMS{{tab_id}};


$scope.{{ tab_id }}editItem = function(item) {
    {% block edit %}
    {% endblock %}
    $scope.{{ tab_id }}openToAdd(item);
};

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
$scope.{{ tab_id }}openToAdd = function(item) {
    var obj = item;

    var modalInstance = $modal.open({
        templateUrl: '{{ modal_id }}',
        controller: '{{ modal_ctrl }}',
        size: 'lg',
        backdrop: 'static',
        resolve: {
            object: function() {
                return obj;
            }
        }
    });

    modalInstance.result.then(function (selected) {
        if (obj) {
            var index = ITEMS{{tab_id}}.indexOf(item);
            ITEMS{{tab_id}}[index] = selected;
        } else {
            ITEMS{{tab_id}}.push(selected);
        }
        $scope.items.{{ tab_id }}ITEMS = ITEMS{{tab_id}};


    }, function () {
        console.log("THEN2");
    });
};