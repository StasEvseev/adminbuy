$scope.extra_flds = {};
$scope.extra_flds.btn_1_show = false;
$scope.extra_flds.btn_2_show = false;
$scope.extra_flds.btn_3_show = false;
$scope.extra_flds.btn_4_show = false;
$scope.extra_flds.btn_5_show = false;

$scope.extra_flds.btn_click = function(status) {
    if (status == {{status}}) {
        bootbox.confirm("Вы уверены, что хотите перевести запись в финальный статус? Внимание! Это необратимое изменение.",
            function(result) {
                if (result) {
                    _save(clbk_const(status));
                }
        });
    } else {
        _save(clbk_const(status))
    }
};

function clbk_const(status) {
    var a = status;
    return function(object) {
        {{ name }}RES_STATUS.meth({id: object.id, data: {
            'status': status
        }},
        function(data) {
            $route.reload();
        }, function (data) {
            toastr.error(data.data.message, 'Ошибка сохранения!');
        });
    };
}