/*global define*/

define([
    'jquery',
    'underscore',
    'backbone',
    'templates'
], function ($, _, Backbone, JST) {
    'use strict';

    var KeyValueView = Backbone.View.extend({

        tagName: 'tr',

        template: JST['app/scripts/templates/keyvalue.ejs'],

        events: {
            'blur input': 'update',
            'click button': 'clear'
        },

        initialize: function () {
            this.listenTo(this.model, 'destroy', this.remove);
        },

        render: function() {
            this.$el.html( this.template( this.model.toJSON() ) );
            return this;
        },

        update: function() {
            var key = this.$('input[name="key"]').val(),
                value = this.$('input[name="value"]').val();
            this.model.set({key: key, value: value});
        },

        clear: function() {
            this.model.destroy();
        }
    });

    return KeyValueView;
});
