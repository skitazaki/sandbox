/*global define*/

define([
    'underscore',
    'backbone'
], function (_, Backbone) {
    'use strict';

    var PointModel = Backbone.Model.extend({

        defaults: {
            'lat': null,
            'lng': null,
            'grid': {}
        },

        initialize: function (options) {
            var url = options.urlRoot;
            this.urlRoot = url +
                (url.charAt(url.length - 1) === '/' ? '' : '/') +
                'coordinates/';
        },

        url: function() {
            var lat = this.get('lat'),
                lng = this.get('lng');
            return this.urlRoot + lat + ',' + lng;
        }
    });

    return PointModel;
});
