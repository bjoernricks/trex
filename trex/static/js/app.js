var trexApp = angular.module('trexApp', ['ngRoute', 'trexControllers']);

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
            otherwise({
                redirectTo: 'projects/'
            });
    }]
);

