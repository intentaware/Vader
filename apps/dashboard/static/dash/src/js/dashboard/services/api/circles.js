'use strict';

angular.module('adomattic.dashboard')
  .factory('Circle', function($resource, urls) {
    return $resource(
      urls.apiBaseUrl + 'companies/circles/:id:list/:doc/',
      {
        id: '@id',
        doc: '@doc',
        list: '@list'
      }, {
        update: {
          method: 'PUT',
          isArray: false
        }
      }
    );
  });
