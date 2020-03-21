/*global define*/

define([
    'jquery',
    'underscore',
    'backbone',
    'templates'
], function ($, _, Backbone, JST) {
    'use strict';

    var HeaderView = Backbone.View.extend({

        template: JST['app/scripts/templates/header.ejs'],

        events: {
            'click a[href="#paste"]': 'viewPaste',
            'click a[href="#bookmarklet"]': 'viewBookmarklet'
        },

        initialize: function () {
        },

        render: function() {
            this.$el.html( this.template() );
            return this;
        },

        viewPaste: function(e) {
            var $e = $(e.target);
            if ($e.text() === 'Open') {
                $e.text('Close');
            } else {
                $e.text('Open');
            }
            this.trigger('toggleCriteria');
        },

        viewBookmarklet: function() {
            this.trigger('showDialog', 'bookmarklet');
        }

    });

    return HeaderView;
});
