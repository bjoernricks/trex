var trexServices = angular.module('trexServices', ['ngResource']);

trexServices.factory('Project', ['$resource',
    function($resource) {
        return $resource('/api/1/projects/:projectId', {projectId: '@id'}, {
            entries: {method: 'GET', isArray: true,
                      url: '/api/1/projects/:projectId/entries',
                      params: {projectId:'@id'}
                     }
        });
    }
]);

trexServices.factory('Entry', ['$resource',
    function($resource) {
        return $resource('/api/1/entries/:entryId', {entryId: '@id'}, {
        });
    }
]);
