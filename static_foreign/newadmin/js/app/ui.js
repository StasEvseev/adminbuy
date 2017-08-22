AdminApp.run(function($rootScope) {

});

AdminApp.directive('icheck', function() {
    return {
        link: function(scope, element, attr) {
            element.iCheck({
              checkboxClass: 'icheckbox_minimal-red',
              radioClass: 'iradio_minimal-red'
            });
        }
    }
});

AdminApp.directive('tree', function() {
    return {
        link: function(scope, element, attr) {

            $("li a", element).on('click', function (e) {
              //Get the clicked link and the next element
              var $this = $(this);
              var checkElement = $this.next();

              //Check if the next element is a menu and is visible
              if ((checkElement.is('.treeview-menu')) && (checkElement.is(':visible'))) {
                //Close the menu
                checkElement.slideUp('normal', function () {
                  checkElement.removeClass('menu-open');
                  //Fix the layout in case the sidebar stretches over the height of the window
                  //_this.layout.fix();
                });
                checkElement.parent("li").removeClass("active");
              }
              //If the menu is not visible
              else if ((checkElement.is('.treeview-menu')) && (!checkElement.is(':visible'))) {
                //Get the parent menu
                var parent = $this.parents('ul').first();
                //Close all open menus within the parent
                var ul = parent.find('ul:visible').slideUp('normal');
                //Remove the menu-open class from the parent
                ul.removeClass('menu-open');
                //Get the parent li
                var parent_li = $this.parent("li");

                //Open the target menu and add the menu-open class
                checkElement.slideDown('normal', function () {
                  //Add the class active to the parent li
                  checkElement.addClass('menu-open');
                  parent.find('li.active').removeClass('active');
                  parent_li.addClass('active');
                  //Fix the layout in case the sidebar stretches over the height of the window
//                  _this.layout.fix();
                    $.AdminLTE.layout.fix();
                });
              } else {
                  parent = $this.parent("li");
                  ul_core = parent.parent("ul");
                  var active = ul_core.find("li.active");
                  ul = active.find("ul:visible").slideUp("normal");

                  active.removeClass('active');
                  ul.removeClass('menu-open');

                  parent.addClass('active');

              }
              //if this isn't a link, prevent the page from being redirected
              if (checkElement.is('.treeview-menu')) {
                e.preventDefault();
              }
            });
        }
    }
});

AdminApp.directive('myAutoPadding', ['$document', "$rootScope", function($document, $rootScope) {
  return {
    link: function(scope, element, attr) {

      var handl = function() {

        var prev = element.prev();
        if (prev) {
            var height = prev.height();
            element.css("padding-top", height + 15);
        }
      };

        $document.on("resize", handl);

        $rootScope.$on('$viewContentLoaded',
        function(event, toState, toParams, fromState, fromParams){
            handl();
        });

        handl();
    }
  };
}]);

AdminApp.directive('contentWr', function() {
    return {
        link: function(scope, element) {
            var window_height = $(window).height();
            if ($("body").hasClass("fixed")) {
                element.css('min-height', window_height - $('.main-footer').outerHeight());
            }
        }
    }
});

AdminApp.directive("headerFixedScroll", function($document, $window, $timeout) {
    return {
        link: function(scope, element) {
            var f_el = $('*').filter(function() {return $(this).css("position") === 'fixed';}).last();
            var f_el_top = f_el.position()['top'] + f_el.height();
            var window_scroll_top;
            var flatElement;
            var topFlatElement;

            var func_resize = function() {
                f_el_top = f_el.position()['top'] + f_el.height();
                resizeTh(true);
                if (flatElement) {
                    flatElement.css('top', f_el_top);
                }
            };

            var func_scroll = function() {
                var topOriginal = element[0].getClientRects()[0].top;

                if (flatElement) {
                    topFlatElement = flatElement[0].getClientRects()[0].top;
                }

                if (topOriginal < f_el_top) {

                    if (!angular.isDefined(window_scroll_top)) {
                        flatElement = $(element[0].cloneNode(true));
                        flatElement.removeAttr("header-fixed-scroll");
                        flatElement.css('position', 'fixed');
                        flatElement.css('top', f_el_top);
                        flatElement.css('z-index', 98);

                        resizeTh();

                        element.parent().append(flatElement);
                        window_scroll_top = $document.scrollTop();
                    }

                }
                else if (topFlatElement && topFlatElement == f_el_top) {
                    if($document.scrollTop() < window_scroll_top) {
                        window_scroll_top = undefined;
                        flatElement.remove();
                        flatElement = undefined;
                    }
                }
            };

            var unwatch = scope.$watch(function() {
                return angular.element(element.parent().parent())[0].rows.length;
            }, function() {
                $timeout(func_resize, 0);
            });

            angular.element($window).on('resize', func_resize);
            $document.on('scroll', func_scroll);

            scope.$on('$destroy', function() {
                angular.element($window).off('resize', func_resize);
                $document.off('scroll', func_scroll);
                unwatch();
            });

            function resizeTh(res) {
                if (flatElement) {
                    for(var i = 0; i < element.children().length; i++) {
                        var child = $(element.children()[i]);
                        var width = child.innerWidth();
                        if (res) {
                            width = child.width();
                        }
                        $(flatElement.children()[i]).width(width);
                    }
                }
            }
        }
    }
});

AdminApp.factory('ConfigWidgets', function() {
    return {
        defaultConfigDatepicker: function(attr_value) {

            var conf = {};

            conf.datepickers = {
                dt: false
            };
            conf.today = function() {
                attr_value = new Date();
            };
            conf.today();
            conf.showWeeks = true;
            conf.toggleWeeks = function () {
                conf.showWeeks = ! conf.showWeeks;
            };
            conf.clear = function () {
                attr_value = null;
            };
            conf.toggleMin = function() {
                conf.minDate = ( conf.minDate ) ? null : new Date();
            };
            conf.toggleMin();
            conf.open = function($event, condition_func) {
                if (angular.isUndefined(condition_func) || !angular.isUndefined(condition_func) && !condition_func()) {
                    conf.status.opened = true;
                }
            };
            conf.status = {
                opened: false
            };
            conf.dateOptions = {
                'year-format': "'yy'",
                'starting-day': 1
            };

            return conf;
        }
    }
});