// -*- coding: utf-8 -*-
//
// (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
//
// See LICENSE comming with the source of 'trex' for details.
//
'use strict';

var trexDirectives = angular.module('trex.directives', []);

trexDirectives.directive('ngEnter', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            element.bind("keydown", function(event) {
                if (event.which === 13) {
                    scope.$apply(function() {
                        scope.$eval(attrs.ngEnter);
                    });
                    event.preventDefault();
                }
            });
        }
    };
});

trexDirectives.directive('fileUpload', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            element.bind('change', function(event) {
                var files = event.target.files;
                 for (var i = 0; i < files.length; i++) {
                     scope.$emit("fileSelected", { file: files[i] });
                 }
            });
        }
    };
});
