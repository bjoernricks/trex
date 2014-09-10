var trexControllers = angular.module('trexControllers', []);

trexControllers.controller('ProjectListCtrl', ['$scope', '$http',
    function($scope, $http) {
        $http.get('/api/1/projects/').success(function(data) {
            $scope.projects = data;
        });

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
    ['$scope', '$routeParams', '$http',
    function($scope, $routeParams, $http) {
        $http.get('/api/1/projects/' + $routeParams.id).success(function(data) {
            $scope.project = data;
        });
    }
]);
