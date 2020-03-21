/*global define*/

define([
    'jquery',
    'underscore',
    'backbone',
    'templates'
], function ($, _, Backbone, JST) {
    'use strict';

    var FooterView = Backbone.View.extend({

        template: JST['app/scripts/templates/footer.ejs'],

        events: {
            'click #view-json': 'viewJson',
            'click #view-url': 'viewUrl',
            'click #view-curl': 'viewCurl',
            'click #send-request': 'sendRequest'
        },

        initialize: function () {
        },

        render: function() {
            this.$el.html( this.template() );
            return this;
        },

        viewJson: function() {
            this.trigger('showDialog', 'json');
        },

        viewUrl: function() {
            this.trigger('showDialog', 'url');
        },

        viewCurl: function() {
            this.trigger('showDialog', 'curl');
        },

        sendRequest: function() {
            this.trigger('sendRequest');
        }
    });

    return FooterView;
});
