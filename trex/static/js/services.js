// -*- coding: utf-8 -*-
//
// (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
//
// See LICENSE comming with the source of 'trex' for details.
//
'use strict';

var trexServices = angular.module('trex.services', ['ngResource']);


trexServices.factory('Conf', function($location) {
    function getRootUrl() {
        var rootUrl = $location.protocol() + '://' + $location.host();
        if ($location.port())
            rootUrl += ':' + $location.port();
        return rootUrl;
    };

    return {
        'apiBase': '/api/1',
        'rootUrl': getRootUrl()
    };
});

trexServices.factory('Project', ['$resource', 'Conf',
    function($resource, Conf) {
        return $resource(Conf.apiBase + '/projects/:projectId/',
            {projectId: '@id'},
            {entries: {method: 'GET', isArray: true,
                       url: Conf.apiBase + '/projects/:projectId/entries/',
                       params: {projectId: '@id'}
                      },
             tags: {method: 'GET', isArray: true,
                    url: Conf.apiBase + '/projects/:projectId/tags/',
                    params: {projectId: '@id'}
                   },
             users: {method: 'GET', isArray: true,
                     url: Conf.apiBase + '/projects/:projectId/users/',
                     params: {projectId: '@id'}
                    }
           }
        );
    }
]);

trexServices.factory('Entry', ['$resource', 'Conf',
    function($resource, Conf) {
        return $resource(Conf.apiBase + '/entries/:entryId/', {entryId: '@id'},
            {}
        );
    }
]);
