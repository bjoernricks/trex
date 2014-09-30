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
            return "" + hours + ":0" + minutes + " h";
        }
        return "" + hours + ":" + minutes + " h";
    };
});

module.filter('workduration', function() {
    return function(input) {
        var minutes = input / 60;
        var hours = Math.floor(minutes / 60);
        var minutes = minutes % 60;
        var ret = "";
        var work_day_hours = 8;

        if (hours >= work_day_hours) {
            var org_hours = hours;
            var days = Math.floor(org_hours / work_day_hours);
            hours = org_hours % work_day_hours;

            ret = "" + days;
            if (days > 1) {
                ret = ret + " days ";
            }
            else {
                ret = ret + "day ";
            }
        }

        if (minutes.toString().length < 2) {
            return ret + hours + ":0" + minutes + " h";
        }
        return ret + hours + ":" + minutes + " h";
    };
});

module.filter('sumByKey', function() {
    return function(data, key) {
        if (typeof(data) === 'undefined' || typeof(key) === 'undefined') {
            return 0;
        }

        var sum = 0;
        for (var i = data.length - 1; i >= 0; i--) {
            sum += parseInt(data[i][key]);
        }

        return sum;
    };
});

module.filter('kb', function() {
    return function(data) {
        if (typeof(data) === 'undefined') {
            return 0;
        }

        return data / 1024;
    };
});
