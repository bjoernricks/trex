var trexControllers = angular.module('trexControllers', []);

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
        // $http.get('/api/1/projects/' + $routeParams.id + "/entries").success(
        //     function(data) {
        // });
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
