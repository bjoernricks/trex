// -*- coding: utf-8 -*-
//
// (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
//
// See LICENSE comming with the source of 'trex' for details.
//
'use strict';

var trexApp = angular.module('trex.app',
        ['ngRoute', 'ngCookies', 'trex.controllers', 'trex.filters',
         'trex.services']);

trexApp.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when("/projects/", {
                templateUrl: 'static/html/projects.html',
                controller: 'ProjectListCtrl'
            }).
            when("/projects/:id", {
                templateUrl: 'static/html/project-detail.html',
                controller: 'ProjectDetailCtrl'
            }).
            when("/entries/:id", {
                templateUrl: 'static/html/entry-detail.html',
                controller: 'EntryDetailCtrl'
            }).
            otherwise({
                redirectTo: '/'
            });
    }]
);

trexApp.run(['$http', '$cookies',
    function($http, $cookies) {
        $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
    }]
);

