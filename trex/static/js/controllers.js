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

        $scope.entries_tags = "";

        $scope.order = "id";
        $scope.orderreverse = false;

        $scope.$watch('project.$resolved', function(value) {
            $scope.project_loading = !value;
        });

        $scope.$watch('entries.$resolved', function(value) {
            $scope.entries_loading = !value;
        });

        $scope.setOrder = function(name) {
            if (name == $scope.order) {
                $scope.orderreverse = !$scope.orderreverse;
            }
            $scope.order = name;
        };

        $scope.searchEntries = function() {
            $scope.entries = Project.entries(
                    {
                        projectId: $routeParams.id,
                        from_date: $scope.entries_from_date,
                        to_date: $scope.entries_to_date,
                        state: $scope.entries_state,
                        tag: $scope.entries_tags
                    }
                );
            $scope.entries_loading = true;
        };

        $scope.addSearchTag = function(tag) {
            if ($scope.entries_tags.indexOf(tag) == -1) {
                if ($scope.entries_tags.length == 0) {
                  $scope.entries_tags += tag;
                }
                else {
                  $scope.entries_tags += "," + tag;
                }
            }
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
