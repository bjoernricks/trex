// -*- coding: utf-8 -*-
//
// (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
//
// See LICENSE comming with the source of 'trex' for details.
//
'use strict';

var trexServices = angular.module('trex.services', ['ngResource']);

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
