/*global define*/

define([
    'jquery',
    'underscore',
    'backbone',
    'purl',
    'ecljs',
    'templates'
], function ($, _, Backbone, purl, ECL, JST) {
    'use strict';

    var CriteriaView = Backbone.View.extend({

        tagName: 'form',

        template: JST['app/scripts/templates/criteria.ejs'],

        events: {
            'submit': 'parse',
            'click .alert button': 'hideAlert'
        },

        initialize: function () {
        },

        render: function() {
            this.$el.hide();
            this.$el.html( this.template() );
            return this;
        },

        parse: function(e) {
            e.preventDefault();
            var input = this.$('input[name="q"]'),
                allowEmpty = this.$('input[name="allow-empty"]:checked').val(),
                text = input.val().trim();
            if (text !== '') {
                var url;
                try {
                    url = purl(text);
                } catch(ex) {
                    // URIError is thrown from `decodeURI()` under `purl()`.
                    // Assume the reason is that character set is not "utf8".
                    url = purl(ECL['Unescape' + ECL['GetEscapeCodeType'](text)](text));
                }
                input.val('');
                var protocol = url.attr('protocol');
                if (protocol && protocol !== 'http' && protocol !== 'https') {
                    this.$('.alert p').text('Invalid Protocol: ' + protocol);
                    this.$('.alert').show();
                } else {
                    this.trigger('parsed', url, allowEmpty);
                }
            } else {
                input.addClass('alert-error');
                setTimeout(function() {
                    input.removeClass('alert-error');
                }, 3000);
            }
        },

        hideAlert: function() {
            this.$('.alert').hide();
        }
    });

    return CriteriaView;
});
