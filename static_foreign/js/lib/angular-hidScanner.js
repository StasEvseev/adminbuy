/**
 * Author: Furqan Razzaq
 * License: MIT
 * Date: June 23, 2014
 */
//(function(window, angular){'use strict';

//    angular.module('angular-hidScanner', []).
//
//    factory('hidScanner', function($rootScope, $window, $timeout) {
//        return {
//            initialize : function() {
//                var chars = [];
//                var pressed = false;
//                angular.element($window).on('keypress', function(e) {
//                    if (e.which >= 48 && e.which <= 57) {
//                        chars.push(String.fromCharCode(e.which));
//                    }
//                    // console.log(e.which + ":" + chars.join("|"));
//                    if (pressed == false) {
//                        $timeout(function(){
//                            if (chars.length >= 10) {
//                                var barcode = chars.join("");
//                                $rootScope.$broadcast("hidScanner::scanned", {barcode: barcode});
//                            }
//                            chars = [];
//                            pressed = false;
//                        },250);
//                    }
//                    pressed = true;
//                });
//            }
//        };
//    })

//    run(function($rootScope){
//            debugger
//        $rootScope.$on("hidScanner::scanned", function(event, args) {
//            // write your logic here ..., args.barcode contains the barcode being received from the scanner
//            $rootScope.$apply();
//        });
//    });

//})(window, window.angular);
