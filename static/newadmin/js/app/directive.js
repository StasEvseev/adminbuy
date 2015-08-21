/**
 * Created by user on 04.08.15.
 */

angular.module('directive', []).directive('dictSelectField', function($compile, $modal) {
    return {
        restrict: 'E',
        transclude: true,
        require: ["^ngModel"],
        scope: {
            service: "=",
            lazy: "&",
            select: "=",
            dname: "@",
            drequired: "@",
            dngRequired: "@"
        },
        templateUrl: 'static/newadmin/template/directive/dsf.html',
        controller: function($scope, $q) {
            $scope.modelsss = {};

            var lazy =  $q.defer();

            $scope.open = function() {
                lazy.resolve();
            };

            $scope.select_item = function() {
                $scope.select = $scope.modelsss.item.id;
            };

            $scope.refresh = function(text) {
                if($scope.lazy()) {
                    lazy.promise.then(function() {
                        $scope.service.records(text).then(function(resp) {
                            $scope.$items = resp;
                        });
                    })
                } else {
                    $scope.service.records(text).then(function(resp) {
                        $scope.$items = resp;
                    });
                }
            };

            $scope.create = function() {
                var modalInstance = $modal.open({
                    template: $scope.service.template(),
                    controller: $scope.service.controller(),
                    size: $scope.service.size(),
                    resolve: $scope.service.resolve()
                });
                modalInstance.result.then(function (model) {
                    $scope.modelsss.item = model;
                }, function () {

                });
            };

            $scope.edit = function() {
                var modalInstance = $modal.open({
                    template: $scope.service.templateEdit(),
                    controller: $scope.service.controllerEdit(),
                    size: $scope.service.size(),
                    resolve: $scope.service.resolveEdit($scope.modelsss.item)
                });
                modalInstance.result.then(function (model) {
                    $scope.modelsss.item = model;
                }, function () {

                });
            }
        },
        compile: function(tElement, tAttrs, transclude) {
            var ngat = tElement.attr('ng-model');
            return function (scope, element, attr, ngModel, transFn) {

                //HUCK
                //прокидываем скоуп в директову... причина - необходмость писать выражения в директивах с
                //model
                scope.model = scope.$parent.model;

                //Следим за изменением модели
                scope.$watch(function () {
                  return ngModel[0].$modelValue;
               }, function(newValue) {
                   scope.modelsss.item = newValue;
               });

                scope.$watch("modelsss.item", function(newValue) {
                    if (ngModel[0].$viewValue !== newValue) {
                        ngModel[0].$setViewValue(newValue);
                    }
                });

                ngModel.$render = function() {
                    scope.modelsss.item = ngModel.$viewValue;
                };

                var uiselect, par;

                transFn(function (clone) {
                    var transcluded = angular.element('<div>').append(clone);
                    var uiselects = element.querySelectorAll('ui-select-s');

                    var transcludedMatch = transcluded.querySelectorAll('dict-select-field-match');
                    var transcludedChoices = transcluded.querySelectorAll('dict-select-field-choices');

                    var uimatchs = uiselects.querySelectorAll('ui-select-match-s'),
                        uichoicess = uiselects.querySelectorAll('ui-select-choices-s'),
                        btns = element.querySelectorAll('div.dsf-btns');

                    uiselect = angular.element('<ui-select>');

                    var uimatch = angular.element('<ui-select-match>'),
                        uichoices = angular.element('<ui-select-choices>');


                    function copyAttr(element1, element2, copytext) {
                        if (!angular.isDefined(element1[0])) {
                            return
                        }
                        var attrs = element1[0].attributes;
                        for (var i = 0; i < attrs.length; i++) {
                            element2.attr(attrs[i].name, element1.attr(attrs[i].name));
                        }
                        if (copytext === true) {
                            element2.html(element1.html());
                        }

                    }

                    if(scope.dname) {
                        uiselect.attr("name", scope.dname);
                        tElement.removeAttr("dname");
                    }
                    if (scope.drequired) {
                        uiselect.attr("required", true);
                        tElement.removeAttr('drequired');
                    }

                    if (scope.dngRequired) {
                        uiselect.attr('ng-required', scope.dngRequired);
                        tElement.removeAttr('dng-required');
                    }

                    copyAttr(uiselects, uiselect);
                    copyAttr(uimatchs, uimatch, true);
                    copyAttr(uichoicess, uichoices, true);

                    copyAttr(transcludedMatch, uimatch, true);
                    copyAttr(transcludedChoices, uichoices, true);

                    uiselect.append(uimatch);
                    uiselect.append(uichoices);

                    par = uiselects.parent();
                    par.children().remove();
                    par.append(uiselect);
                    par.append(btns);
                });

                var fn = $compile(par);
                element.append(fn(scope));
            }
        }
    };
})

.directive('passport', function() {
    return {
        require: 'ngModel',
        link: function(scope, element, attrs, ngModelController) {
            ngModelController.$parsers.push(function(data) {
                //convert data from view format to model format
                var m = data.toString(), datas = data.toString();
                m.replace("/\s/g", "");
                return m; //converted
            });

            ngModelController.$formatters.push(function(data) {
                //convert data from model format to view format
//                var datas = data.toString();
                return parseInt(data, 10);
            });

//            ngModelController.$validators.VAL = function(model, view) {
//                debugger
//                return '/^\d{0}$|^\d{10}$/'.test(model);
//            };
        }
    }
});