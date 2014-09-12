// -*- coding: utf-8 -*-
//
// (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
//
// See LICENSE comming with the source of 'trex' for details.
//
'use strict';

var module = angular.module('trex.filters', []);

module.filter('checkmark', function() {
    return function(input) {
        return input ? '\u2713' : '\u2718';
    };
});

module.filter('duration', function() {
    return function(input) {
        var minutes = input / 60;
        var hours = Math.floor(minutes / 60);
        var minutes = minutes % 60;

        if (minutes.toString().length < 2) {
            return "" + hours + ":0" + minutes;
        }
        return "" + hours + ":" + minutes;
    };
});
