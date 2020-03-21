/*global define*/

define([
    'jquery',
    'backbone'
], function ($, Backbone) {
    'use strict';

    var MainRouter = Backbone.Router.extend({
        routes: {
            'paste': 'showCriteria'
        },

        showCriteria: function() {
            this.trigger('showCriteria');
        }
    });

    return MainRouter;
});
