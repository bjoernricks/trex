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
        $scope.projects_loading = true;

        $scope.projects = Project.query();

        $scope.order = "name";
        $scope.orderreverse = false;

        $scope.$watch('projects.$resolved', function(value) {
            $scope.projects_loading = !value;
        });

        $scope.setOrder = function(name) {
            if (name == $scope.order) {
                $scope.orderreverse = !$scope.orderreverse;
            }
            $scope.order = name;
        };
    }
]);

trexControllers.controller('ProjectCreateCtrl', ['$scope', '$location',
        '$timeout', 'Project', function($scope, $location, $timeout, Project) {

        $scope.succes = false;
        $scope.error = false;

        $scope.successCreate = function(value, headers) {
            $scope.success = true;
            $timeout(function() {
                $location.path('/projects/' + value.id);
            }, 2000);
        };

        $scope.failCreate = function(response) {
            console.error(response);
            $scope.error = true;
            $("#error-frame").html(response.data);
        };

        $scope.createProject = function() {
            $scope.succes = false;
            $scope.error = false;

            var project = new Project();

            project.name = $scope.name;
            project.description = $scope.description;
            project.active = true;

            Project.save(project, $scope.successCreate, $scope.failCreate);
        };

    }
]);

trexControllers.controller('ProjectDetailCtrl',
    ['$scope', '$routeParams', 'Project', '$http', 'Conf',
    function($scope, $routeParams, Project, $http, Conf) {
        $scope.project_loading = true;
        $scope.entries_loading = true;

        $scope.succes = false;
        $scope.error = false;

        $scope.project = Project.get({projectId: $routeParams.id});
        $scope.entries = Project.entries({projectId: $routeParams.id});

        $scope.entries_tags = [];
        $scope.entries_user_abbr = [];

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

        $scope.tagList = function(tags, attr) {
            var search = "";
            angular.forEach(tags, function(value, key) {
                search += value[attr] + ',';

            });
            return search;
        };

        $scope.searchEntries = function() {
            $scope.entries = Project.entries(
                    {
                        projectId: $routeParams.id,
                        from_date: $scope.entries_from_date,
                        to_date: $scope.entries_to_date,
                        state: $scope.entries_state,
                        user_abbr: $scope.tagList($scope.entries_user_abbr, "user_abbr"),
                        tag: $scope.tagList($scope.entries_tags, "name"),
                        tag_like: $scope.entries_tags_like,
                        description: $scope.entries_description,
                        workpackage_like: $scope.entries_workpackage
                    }
                );
            $scope.entries_loading = true;
        };

        $scope.addSearchTag = function(tag) {
            for(var i = 0; i < $scope.entries_tags.length; i++) {
                var value = $scope.entries_tags[i];
                if (value.name == tag) {
                    return;
                }
            };
            $scope.entries_tags.push({'name': tag});
        };

        $scope.addUser = function(user) {
            for(var i = 0; i < $scope.entries_user_abbr.length; i++) {
                var value = $scope.entries_user_abbr[i];
                if (value.user_abbr == user.user_abbr) {
                    return;
                }
            };
            $scope.entries_user_abbr.push(user);
        };

        $scope.completeTag = function(query) {
            return Project.tags(
                    {
                        projectId: $routeParams.id,
                        name_like: query
                    }).$promise;
        };

        $scope.completeUser = function(query) {
            return Project.users(
                    {
                        projectId: $routeParams.id,
                        user_abbr_like: query
                    }).$promise;
        };

        $scope.zeiterfassung_files = [];

        $scope.$on("fileSelected", function(event, args) {
            $scope.$apply(function() {
                $scope.zeiterfassung_files.push(args.file);
            });
        });

        $scope.uploadFiles = function() {
            $scope.resetDialogs();
             var fileReader = new FileReader();
             fileReader.onload = function(e) {
                 console.log(e.target.result);
                 $http({
                     method: 'POST',
                     headers: { 'Content-Type': 'text/plain'},
                     url: Conf.apiBase + '/projects/' + $routeParams.id +
                     '/zeiterfassung/',
                     data: e.target.result
                 }).
                 success(function(data, status, headers, config) {
                     $scope.zeiterfassung_files = [];
                     $scope.showSuccess(
                         'Upload successfull. ' + data['written'].length +
                         ' new entries loaded. ' + data['skipped'].length +
                         ' entries skipped.');
                     $scope.searchEntries();
                 }).
                 error(function(data, status, headers, config) {
                     $scope.showError("Upload failed", data);
                 });
             };
             for (var i = 0; i < $scope.zeiterfassung_files.length; i++) {
                fileReader.readAsBinaryString($scope.zeiterfassung_files[i]);
             }

        };

        $scope.resetDialogs = function() {
            $scope.error = false;
            $scope.success = false;
        };

        $scope.showSuccess = function(message) {
            $scope.success = true;
            $scope.success_message = message;
        };

        $scope.showError = function(message, data) {
            $scope.error = true;
            $scope.error_message = message;
            if (data) {
                $("#error-frame").html(data);
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
