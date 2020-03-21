/*global define*/

define([
    'jquery',
    'underscore',
    'backbone',
    'templates'
], function ($, _, Backbone, JST) {
    'use strict';

    var PointView = Backbone.View.extend({

        template: JST['app/scripts/templates/point.ejs'],

        events: {
            'blur input': 'updateCoordinates'
        },

        initialize: function () {
            this.listenTo(this.model, 'change', this.render);
            this.listenTo(this.model, 'destroy', this.remove);
            this.render();
        },

        render: function() {
            var props = this.model.toJSON();
            props.gridLevel = this.grid;
            this.$el.html( this.template( props ) );
            return this;
        },

        clear: function() {
            this.model.destroy();
        },

        setGridLevel: function(grid) {
            this.grid = grid;
        },

        updateCoordinates: function(e) {
            var elem = $(e.target),
                name = elem.attr('name'),
                val = elem.val();
            if (!val) {
                return;
            }
            var v = parseFloat(val);
            if (!v) {
                elem.val('');
                return;
            }
            // TODO: Check Japanese grid mesh boundary.
            // TODO: Compare the value of before and after.
            if (name === 'lat') {
                this.model.set('lat', v);
            } else if (name === 'lng') {
                this.model.set('lng', v);
            }
            this.model.fetch();
        }

    });

    return PointView;
});
