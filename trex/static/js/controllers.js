// -*- coding: utf-8 -*-
//
// (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
//
// See LICENSE comming with the source of 'trex' for details.
//
'use strict';

var trexControllers = angular.module('trex.controllers', []);

trexControllers.controller('ProjectListCtrl', ['$scope', 'Project',
    function($scope, Project) {
        $scope.projects = Project.query();

        $scope.order = "name";
        $scope.orderreverse = false;

        $scope.setOrder = function(name) {
            if (name == $scope.order) {
                $scope.orderreverse = !$scope.orderreverse;
            }
            $scope.order = name;
        };
    }
]);

trexControllers.controller('ProjectDetailCtrl',
    ['$scope', '$routeParams', 'Project',
    function($scope, $routeParams, Project) {
        $scope.project = Project.get({projectId: $routeParams.id});
        $scope.entries = Project.entries({projectId: $routeParams.id});

        $scope.order = "id";
        $scope.orderreverse = false;

        $scope.$watch('entries.$resolved', function(value) {
            $scope.loading = !value;
        });

        $scope.setOrder = function(name) {
            if (name == $scope.order) {
                $scope.orderreverse = !$scope.orderreverse;
            }
            $scope.order = name;
        };
    }
]);

trexControllers.controller('EntryDetailCtrl',
    ['$scope', '$routeParams', 'Entry',
    function($scope, $routeParams, Entry) {
        $scope.entry = Entry.get({entryId: $routeParams.id});

        $scope.order = "id";
        $scope.orderreverse = false;

        $scope.setOrder = function(name) {
            if (name == $scope.order) {
                $scope.orderreverse = !$scope.orderreverse;
            }
            $scope.order = name;
        };
    }
]);
