angular.module('ElemsModule', ['ngTable', 'TableHelper'])

    .directive("topPanel", function() {
        return {
            restrict: "E",
            templateUrl: "/___old/template/elems/topPanel.html",
            transclude: true,
            scope: {
                breadcrumbs: "="
            }
        }
    })

    .directive("searchField", function() {
            return {
                restrict: "E",
                templateUrl: "/___old/template/elems/searchField.html",
                scope: {
                    placeholder: "@",
                    clbkclick: "="
                }
            }
    })

    .directive("dateField", function() {
        return {
            restrict: "E",
            templateUrl: "/___old/template/elems/date.html",
            scope: {
                label: "@",
                model: "=",
                disabled: "="
            },
            controller: function($scope) {
                $scope.today = function() {
                    $scope.model.dt = new Date();
                };
                if (!$scope.model.dt) {
                    $scope.today();
                }


                $scope.clear = function () {
                    $scope.model.dt = null;
                };

                //scope.;

                $scope.disabledDate = function(date, mode) {
                    return ( mode === 'day' && ( date.getDay() === 0 || date.getDay() === 6 ) );
                };

                $scope.toggleMin = function() {
                    $scope.model.minDate = $scope.model.minDate ? null : new Date();
                };
                $scope.toggleMin();

                $scope.open = function($event) {
                    $event.preventDefault();
                    $event.stopPropagation();

                    $scope.opened = true;
                };

                $scope.dateOptions = {
                    formatYear: 'yy',
                    startingDay: 1
                };

                $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
                $scope.format = $scope.formats[0];
            }
        }
    })

    .directive("dateFieldBr", function() {
        return {
            restrict: "E",
            templateUrl: "/___old/template/elems/datebr.html",
            scope: {
                label: "@",
                model: "=",
                disabled: "="
            },
            controller: function($scope) {
                $scope.data = {};
                $scope.today = function() {
                    $scope.data.dt = new Date();
                    $scope.model = $scope.data.dt;
                };
                if (_.isEmpty($scope.model)) {
                    $scope.today();
                }

                $scope.$watch('model', function(newValue, oldValue){
                    $scope.data.dt = newValue;
                });

                $scope.$watch('data.dt', function(newValue, oldValue) {
                    $scope.model = newValue;
                });


                $scope.clear = function () {
                    $scope.data.dt = null;
                    $scope.model = null;
                };

                //scope.;

                $scope.disabledDate = function(date, mode) {
                    return ( mode === 'day' && ( date.getDay() === 0 || date.getDay() === 6 ) );
                };

                $scope.toggleMin = function() {
                    $scope.data.minDate = $scope.data.minDate ? null : new Date();
                };
                $scope.toggleMin();

                $scope.open = function($event) {
                    $event.preventDefault();
                    $event.stopPropagation();

                    $scope.opened = true;
                };

                $scope.dateOptions = {
                    formatYear: 'yy',
                    startingDay: 1
                };

                $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
                $scope.format = $scope.formats[0];
            }
        }
    })

    .directive("tableRemote", function (ngTableParams, load, $compile) {
        return {
            restrict: "E",
            transclude: "element",
            scope: {
                "class": "@",
                resource: "=",
                selected: "=",
                handlerclkrow: "=",
                load: "=",
                filterField: "@"
            },
            priority: 1000,
            controller: function($scope) {
                $scope.model = {};

                $scope.model.filter_field = $scope.filterField;

                if ($scope.selected) {
                    $scope.setSelected = function (selected) {
                       $scope.model.idSelected = selected.id;
                       $scope.model.selected = selected;
                        $scope.selected = selected;
                    };
                    $scope.model.idSelected = null;
                }

                $scope.tableParams = new ngTableParams({
                    page: 1,            // show first page
                    count: 10,
                    sorting: {
                             // initial sorting
                    }
                }, {
                    counts: [],
                    total: 0,           // length of data
                    getData: function($defer, params) {

                        $scope.model.count = params.count();

                        $scope.model.page = params.page();

                        load.loadData(function(data) {
                            params.total(data.max);
                            $defer.resolve(data.items);
                        }, $scope.resource, {}, $scope);
                    }
                });

                $scope.load = function(text) {
                    $scope.model.filter_text = text;
                    $scope.tableParams.reload();
                };
            },
            link: function(scope, iElement, iAttrs, controller, transcludeFn) {

                var attrReplace = function(el, attr) {
                    if (attr.name.length > 2 && attr.name.substring(0, 2) == "r-") {
                        el.attr("ng-" + attr.name.substring(2, attr.name.length), el.attr(attr.name));
                    }
                };

                var attrRec = function(el) {
                    angular.forEach(el.children(), function(ch) {
                        var attrs = ch.attributes;
                        ch = angular.element(ch);
                        angular.forEach(attrs, function(attr) {
                            attrReplace(ch, attr);
                        });
                    })
                };

                var els = transcludeFn();
                var tr = angular.element("<tr></tr>");

                if(scope.handlerclkrow) {
                    tr.attr("ng-click", "handlerclkrow(item)")
                } else if (scope.selected) {
                    tr.attr("ng-click", "setSelected(item)");
                }

                var row = els.find("row");
                var attrs = row[0].attributes;

                angular.forEach(attrs, function(at) {
                    tr.attr(at.name, row.attr(at.name));
                    attrReplace(tr, at);
                });
                var tds = els.find("row > column");

                angular.forEach(tds, function(td) {
                    var tdnew = angular.element("<td></td>");
                    var attrs = td.attributes;

                    angular.forEach(attrs, function(at) {
                        tdnew.attr(at.name, angular.element(td).attr(at.name));
                        attrReplace(tdnew, at);
                    });

                    tdnew.append(td.children);
                    attrRec(tdnew);
                    tr.append(tdnew);
                });

                var columns_count = tds.length;

                var table = angular.element("<table ng-cloak ng-table=\"tableParams\" class=\"{{ class }}\"></table>");
                var tbody = angular.element("<tbody><tr ng-repeat=\"it in [] | range: 4 - $data.length\"><td colspan="+ columns_count +">&nbsp;</td></tr></tbody>");
                var tfoot = angular.element("<tfoot><tr></tr></tfoot>");
                table.append(tbody);
                table.append(tfoot);
                tbody.prepend(tr);

                iElement.after(table);

                $compile(table, transcludeFn)(scope);
            }
        }
    })

    .directive("tableRemoteBr", function (ngTableParams, load, $compile, $location, $window) {
        return {
            restrict: "E",
            transclude: "element",
            scope: {
                "class": "@",
                resource: "=",
                param: "=",
                selected: "=",
                handlerclkrow: "=",
                load: "=",
                filterField: "@",
                ms: "=",
                counts: "=",
                main: "="
            },
            priority: 1000,
            controller: function($scope) {
                $scope.model = {};

                $scope.model.filter_field = $scope.filterField;

                if ($scope.selected) {
                    $scope.setSelected = function (selected) {
                        $scope.model.idSelected = selected.id;
                        $scope.model.selected = selected;
                        $scope.selected = selected;
                    };
                    $scope.model.idSelected = null;
                }

                if ($scope.main) {
                    $scope.tableParams = new ngTableParams(angular.extend({
                        page: 1,            // show first page
                        count: ($scope.param && $scope.param['count']) || 10,
                        sorting: {
                                 // initial sorting
                        }
                    }, $location.search()), {
                        counts: $scope.counts,
                        total: 0,           // length of data
                        getData: function($defer, params) {
                            $location.search(params.url());
                            $scope.model.count = params.count();

                            $scope.model.page = params.page();

                            var parm = $scope.param || {};

                            console.log("getDATA");
                            load.loadData(function(data) {
                                params.total(data.max);
                                $defer.resolve(data.items);
                            }, $scope.resource, parm, $scope);
                        }
                    });
                } else {
                    $scope.tableParams = new ngTableParams({
                        page: 1,            // show first page
                        count: ($scope.param && $scope.param['count']) || 10,
                        sorting: {
                                 // initial sorting
                        }
                    }, {
                        counts: $scope.counts,
                        total: 0,           // length of data
                        getData: function($defer, params) {
                            //$location.search(params.url());
                            $scope.model.count = params.count();

                            $scope.model.page = params.page();

                            var parm = $scope.param || {};

                            console.log("getDATA");
                            load.loadData(function(data) {
                                params.total(data.max);
                                $defer.resolve(data.items);
                            }, $scope.resource, parm, $scope);
                        }
                    });
                }



                $scope.checkboxes = { 'checked': false, items: {} };
                $scope.ms = [];

                // watch for check all checkbox
                $scope.$watch('checkboxes.checked', function(value) {
                    angular.forEach($scope.tableParams.data, function(item) {
                        $scope.ms = [];
                        if (angular.isDefined(item.id)) {
                            $scope.checkboxes.items[item.id] = value;
                            $scope.ms.push(item);
                        }
                    });
                });

                // watch for data checkboxes
                $scope.$watch('checkboxes.items', function(values) {
                    $scope.ms = [];
                    if (!$scope.tableParams.data.length) {
                        return;
                    }
                    var checked = 0, unchecked = 0,
                        total = $scope.tableParams.data.length;
                    angular.forEach($scope.tableParams.data, function(item) {
                        if ($scope.checkboxes.items[item.id]) {
                            $scope.ms.push(item);
                        }
                        checked   +=  ($scope.checkboxes.items[item.id]) || 0;
                        unchecked += (!$scope.checkboxes.items[item.id]) || 0;
                    });
                    if ((unchecked == 0) || (checked == 0)) {
                        $scope.checkboxes.checked = (checked == total);
                    }
                    // grayed checkbox
                    angular.element(document.getElementById("select_all")).prop("indeterminate", (checked != 0 && unchecked != 0));
                }, true);

                $scope.load = function(text) {
                    $scope.model.filter_text = text;
                    $scope.tableParams.reload();
                };
            },
            link: function(scope, iElement, iAttrs, controller, transcludeFn) {

                var attrReplace = function(el, attr) {
                    if (attr.name.length > 2 && attr.name.substring(0, 2) == "r-") {
                        el.attr("ng-" + attr.name.substring(2, attr.name.length), el.attr(attr.name));
                    }
                };

                var attrRec = function(el) {
                    angular.forEach(el.children(), function(ch) {
                        var attrs = ch.attributes;
                        ch = angular.element(ch);
                        angular.forEach(attrs, function(attr) {
                            attrReplace(ch, attr);
                        });
                    })
                };

                var els = transcludeFn();
                var tr = angular.element("<tr class='table-row'></tr>");

                if(scope.handlerclkrow) {
                    tr.attr("ng-click", "handlerclkrow(item)")
                } else if (scope.selected) {
                    tr.attr("ng-click", "setSelected(item)");
                }

                var row = els.find("row");
                var attrs = row[0].attributes;

                angular.forEach(attrs, function(at) {
                    tr.attr(at.name, row.attr(at.name));
                    attrReplace(tr, at);
                });
                var tds = els.find("row > column");

                angular.forEach(tds, function(td) {
                    var tdnew = angular.element("<td></td>");
                    var attrs = td.attributes;

                    angular.forEach(attrs, function(at) {
                        tdnew.attr(at.name, angular.element(td).attr(at.name));
                        attrReplace(tdnew, at);
                    });

                    tdnew.append(td.children);
                    attrRec(tdnew);
                    tr.append(tdnew);
                });

                var columns_count = tds.length;

                var table = angular.element("<table ng-cloak ng-table=\"tableParams\" class=\"[[ class ]]\"></table>");
                var tbody = angular.element("<tbody><tr class='table-row-empty' ng-repeat=\"it in [] | range: 4 - $data.length\"><td colspan="+ columns_count +">&nbsp;</td></tr></tbody>");
                var tfoot = angular.element("<tfoot><tr></tr></tfoot>");
                table.append(tbody);
                table.append(tfoot);
                tbody.prepend(tr);

                iElement.after(table);

                $compile(table, transcludeFn)(scope);
            }
        }
    })

    .directive('dictSelectFieldBr', function() {
        return {
            restrict: 'E',
            templateUrl: '/___old/template/elems/dictSelectFieldBr.html',
            scope: {
                id: '@',
                label: '@',
                placeholder: '@',
                modal: '=',
                attrdisplay: '@',
                selected: "=",
                onSelect: "=",
                clbkclose: "=",
                disabled : "=",
                resource: "=",
                isMain: "=",
                canCreate: "=",
                canEdit: "=",
                idForm: "@",
                link: "@"
            },
            controller: function($scope, $modal) {
                $scope.edit = function() {
                    if ($scope.selected) {
                        $scope.createNew(false);
                    }
                };

                $scope.redirect = function(path) {
                    location.href = path;
                };

                $scope.clear = function() {
                    $scope.selected = undefined;
                };

                $scope.refresh = function(text){
                    $scope.loading = true;
                    $scope.reload(text);
                };

                if (angular.isUndefined($scope.disabled)) {
                    $scope.disabled = false;
                }
                $scope.modalMode = true;
                if($scope.modal) {
                    $scope.modalMode = false;
                    var template = $scope.modal[0];
                    var ctrl = $scope.modal[1];
                    var size = $scope.modal.length > 2 ? $scope.modal[2] : 'sm';
                }

                $scope.createNew = function(create) {
                    if ($scope.modal) {
                        var modalInstance;
                        if (create) {
                            modalInstance = $modal.open({
                                templateUrl: template,
                                controller: ctrl,
                                size: size,
                                backdrop: 'static',
                                resolve: {
                                    object: function() {
                                        return undefined;
                                    }
                                }
                            });
                        } else {
                            modalInstance = $modal.open({
                                templateUrl: template,
                                controller: ctrl,
                                size: size,
                                backdrop: 'static',
                                resolve: {
                                    object: function() {
                                        return $scope.selected;
                                    }
                                }
                            });
                        }

                        modalInstance.result.then(function (selected) {
                            $scope.selected = selected;
                            $scope.refresh();
                            if ($scope.clbkclose) {
                                $scope.clbkclose(selected);
                            }
                        }, function () {
                        });
                    }

                };

                $scope.reload = function(text) {
                    if($scope.resource) {
                        $scope.resource({page: 1, count: 10, filter_text: text, filter_field: 'filter_field'}, function(data) {
                            $scope.items = data.items;
                            $scope.loading = false;
                        });
                    }
                };
            },
            link: function($scope, element, attrs) {
                $scope.someFunction = function(obj1, obj2) {
                    $scope.selected = obj1;
                    if ($scope.onSelect) {
                        $scope.onSelect(obj1, obj2);
                    }
                };
            }
        }
    })

    .directive('dictSelectField', function() {
        return {
            restrict: 'E',
            templateUrl: '/___old/template/elems/dictSelectField.html',
            scope: {
                label: '@',
                placeholder: '@',
                modal: '=',
                attrdisplay: '@',
                selected: "=",
                onSelect: "=",
                clbkclose: "=",
                disabled : "=",
                resource: "="
            },
            controller: function($scope, $modal) {
                $scope.edit = function() {
                    if ($scope.selected) {
                        $scope.createNew(false);
                    }
                };

                $scope.refresh = function(text){
                    $scope.reload(text);
                };

                if (angular.isUndefined($scope.disabled)) {
                    $scope.disabled = false;
                }
                $scope.modalMode = true;
                if($scope.modal) {
                    $scope.modalMode = false;
                    var template = $scope.modal[0];
                    var ctrl = $scope.modal[1];
                    var size = $scope.modal.length > 2 ? $scope.modal[2] : 'sm';
                }

                $scope.createNew = function(create) {
                    if ($scope.modal) {
                        var modalInstance;
                        if (create) {
                            modalInstance = $modal.open({
                                templateUrl: template,
                                controller: ctrl,
                                size: size,
                                resolve: {
                                    object: function() {
                                        return undefined;
                                    }
                                }
                            });
                        } else {
                            modalInstance = $modal.open({
                                templateUrl: template,
                                controller: ctrl,
                                size: size,
                                resolve: {
                                    object: function() {
                                        return $scope.selected;
                                    }
                                }
                            });
                        }

                        modalInstance.result.then(function (selected) {
            //                $scope.model.commodity_items.push(selected);
                            $scope.clbkclose(selected);
                        }, function () {
                            console.log("THEN2");
                        });
                    }

                };

                $scope.reload = function(text) {
                    if($scope.resource) {
                        $scope.resource({page: 1, count: 10, filter_text: text, filter_field: 'filter_field'}, function(data) {
                            $scope.items = data.items;
                        });
                    }
                };
            },
            link: function($scope, element, attrs) {
                $scope.someFunction = function(obj1, obj2) {
                    $scope.selected = obj1;
                    if ($scope.onSelect) {
                        $scope.onSelect(obj1, obj2);
                    }
                };
            }
        }
    });