var trexApp = angular.module('trexApp',
        ['ngRoute', 'trexControllers', 'trexFilters', 'trexServices']);

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
