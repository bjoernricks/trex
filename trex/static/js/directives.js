// -*- coding: utf-8 -*-
//
// (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
//
// See LICENSE comming with the source of 'trex' for details.
//
'use strict';

var trexDirectives = angular.module('trex.directives', []);

trexDirectives.directive('trexLoading', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var options = scope.$eval(attrs.trexLoading);
            console.log(options);
            var spinner = new Spinner(options).spin();

            element.append(spinner.el);

            scope.$on('$destroy', function () {
                spinner.stop();
            })

            scope.$watch(attrs.loading, function(value) {
                if (!value) {
                    spinner.stop();
                }
            });

        }
    }
});
