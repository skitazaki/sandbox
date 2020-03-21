/*global define*/

define([
    'jquery',
    'underscore',
    'backbone',
    'templates',
    'bootstrap'
], function ($, _, Backbone, JST) {
    'use strict';

    var AboutView = Backbone.View.extend({

        template: JST['app/scripts/templates/about.ejs'],

        events: {
        },

        initialize: function () {
            this.render();
        },

        render: function() {
            this.$el.html( this.template() );
            return this;
        },

        show: function() {
            this.$('.modal').modal('show', {keyboard: true});
        }

    });

    return AboutView;
});
