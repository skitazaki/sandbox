/*global define*/

define([
    'underscore',
    'backbone'
], function (_, Backbone) {
    'use strict';

    var JpGridModel = Backbone.Model.extend({

        defaults: {
            'properties': null,
            'geometry': null,
            'grid': null
        },

        initialize: function (options) {
            var url = options.urlRoot;
            this.urlRoot = url +
                (url.charAt(url.length - 1) === '/' ? '' : '/') +
                'grid/';
        },

        url: function() {
            return this.urlRoot + this.get('grid');
        }
    });

    return JpGridModel;
});
