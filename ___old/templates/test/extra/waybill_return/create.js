
$scope.extra_flds = {};
$scope.extra_flds.btn_1_show = true;
$scope.extra_flds.btn_2_show = false;
$scope.extra_flds.btn_3_show = false;
$scope.extra_flds.btn_4_show = false;
$scope.extra_flds.btn_5_show = false;
$scope.extra_flds.btn_6_show = false;
$scope.extra_flds.btn_7_show = false;
$scope.extra_flds.btn_8_show = false;
$scope.extra_flds.btn_9_show = false;

$scope.extra_flds.btn_click = function(status) {
    _save(clbk_const(status))
};

function clbk_const(status) {
    return function(object) {
        {{ name }}RES_STATUS.meth({id: object.id, data: {
            'status': status
        }},
        function(data) {
            $location.path(rootUrl + "/" + data.id + "/edit");
//            $location.search({'edit': true});
        }, function (data) {
            toastr.error(data.data.message, 'Ошибка сохранения!');
        });
    };
}

