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

        $scope.search = {};

        $scope.search.entries_tags = [];
        $scope.search.entries_user_abbr = [];

        $scope.order = "id";
        $scope.orderreverse = false;

        $scope.entries_chart = {};
        $scope.entries_chart["data"] = [];
        $scope.entries_chart["types"] = ["Line", "Bar", "Radar"];
        $scope.entries_chart["current_type"] = 0;
        $scope.entries_chart["series"] = ["Duration"];
        $scope.entries_chart["labels"] = [];
        $scope.entries_chart["loaded"] = false;
        $scope.entries_chart["type"] = "Line";
        $scope.entries_chart["options"] = {
            animation: false,
            pointHitDetectionRadius: 5
        };

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
                        from_date: $scope.dateToString(
                            $scope.search.entries_from_date),
                        to_date: $scope.dateToString(
                            $scope.search.entries_to_date),
                        state: $scope.search.entries_state,
                        user_abbr: $scope.tagList(
                            $scope.search.entries_user_abbr, "user_abbr"),
                        tag: $scope.tagList($scope.search.entries_tags, "name"),
                        tag_like: $scope.search.entries_tags_like,
                        description: $scope.search.entries_description,
                        workpackage_like: $scope.search.entries_workpackage
                    }
                );
            $scope.entries_loading = true;

            if ($scope.entries_chart.loaded) {
                $scope.loadChartData();
            }
        };

        $scope.addSearchTag = function(tag) {
            for (var i = 0; i < $scope.search.entries_tags.length; i++) {
                var value = $scope.search.entries_tags[i];
                if (value.name == tag) {
                    return;
                }
            }
            $scope.search.entries_tags.push({'name': tag});
        };

        $scope.addUser = function(user) {
            for (var i = 0; i < $scope.search.entries_user_abbr.length; i++) {
                var value = $scope.search.entries_user_abbr[i];
                if (value.user_abbr == user.user_abbr) {
                    return;
                }
            }
            $scope.search.entries_user_abbr.push(user);
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

        $scope.openFromDatepicker = function($event) {
            $event.preventDefault();
            $event.stopPropagation();

            $scope.opened_from = true;
        };

        $scope.openToDatepicker = function($event) {
            $event.preventDefault();
            $event.stopPropagation();

            $scope.opened_to = true;
        };

        $scope.dateToString = function(date) {
            if (!(date instanceof Date)) {
                return date;
            }

            var dd = date.getDate();
            if (dd < 10) {
                dd = '0' + dd;
            }

            var mm = date.getMonth() + 1;
            if (mm < 10) {
                mm = '0' + mm;
            }

            var yyyy = date.getFullYear();

            return dd + '.' + mm + '.' + yyyy;
        };

        $scope.loadChartData = function() {
            Project.entries_sums(
                {
                    projectId: $routeParams.id,
                    from_date: $scope.dateToString(
                        $scope.search.entries_from_date),
                    to_date: $scope.dateToString(
                        $scope.search.entries_to_date),
                    state: $scope.search.entries_state,
                    user_abbr: $scope.tagList(
                        $scope.search.entries_user_abbr, "user_abbr"),
                    tag: $scope.tagList($scope.search.entries_tags, "name"),
                    tag_like: $scope.search.entries_tags_like,
                    description: $scope.search.entries_description,
                    workpackage_like: $scope.search.entries_workpackage
                }
            ).$promise.then(function(data) {

                var chart_data = [];
                $scope.entries_chart.data = [chart_data];
                $scope.entries_chart.labels = [];
                $scope.entries_chart.loaded = true;

                var workpackage_sums = data["workpackage_sums"];
                for (var i = 0; i < workpackage_sums.length; i++) {
                    var sum = workpackage_sums[i];
                    chart_data.push(sum["duration"]);
                    $scope.entries_chart.labels.push(sum["name"]);
                }
            });

        };

        $scope.entriesChartToggle = function() {
            $scope.entries_chart.current_type += 1;
            if ($scope.entries_chart.current_type >=
                    $scope.entries_chart.types.length) {
                        $scope.entries_chart.current_type = 0;
            }
            $scope.entries_chart.type =
               $scope.entries_chart.types[$scope.entries_chart.current_type];
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
