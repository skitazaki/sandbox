/*global define*/

define([
    'jquery',
    'underscore',
    'backbone',
    'templates',
    'views/keyvalue-view'
], function ($, _, Backbone, JST, KeyValueView) {
    'use strict';

    var KeyValueListView = Backbone.View.extend({

        template: JST['app/scripts/templates/keyvalue-list.ejs'],

        tagName: 'table',
        className: 'table table-condensed table-striped',

        initialize: function () {
            this.listenTo( this.collection, 'add', this.addOne );
            this.listenTo( this.collection, 'reset', this.reset );
        },

        render: function() {
            this.$el.html( this.template() );
            this.collection.each(this.addOne, this);
            return this;
        },

        addOne: function(model) {
            var v = new KeyValueView({model: model});
            this.$('tbody').append( v.render().el );
            this.$el.show();
        },

        reset: function() {
            this.$('tbody').empty();
        }

    });

    return KeyValueListView;
});
