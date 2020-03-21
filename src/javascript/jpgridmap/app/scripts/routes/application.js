/*global define*/

define([
    'jquery',
    'backbone'
], function ($, Backbone) {
    'use strict';

    var ApplicationRouter = Backbone.Router.extend({

        routes: {
            'grid/:grid': 'grid',
            'about': 'about',
            'clear': 'clear'
        }

    });

    return ApplicationRouter;
});
