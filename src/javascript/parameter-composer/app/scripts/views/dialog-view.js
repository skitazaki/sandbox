/*global define*/

define([
    'jquery',
    'underscore',
    'backbone',
    'templates'
], function ($, _, Backbone, JST) {
    'use strict';

    var DialogView = Backbone.View.extend({

        template: JST['app/scripts/templates/dialog.ejs'],

        initialize: function () {
        },

        show: function(options) {
            var params = {};
            params.title = options.title || '';
            params.text = options.text || '';
            params.url = options.url || '';
            this.$el.html( this.template( params ) );
            this.$('.modal').modal();
        }

    });

    return DialogView;
});
