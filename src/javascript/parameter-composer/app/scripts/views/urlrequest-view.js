/*global define*/

define([
    'jquery',
    'underscore',
    'backbone',
    'templates',
    'views/keyvalue-list-view',
    'collections/keyvalue-collection',
    'models/keyvalue-model'
], function ($, _, Backbone, JST, KeyValueListView, KeyValueCollection, KeyValueModel) {
    'use strict';

    var UrlRequestView = Backbone.View.extend({

        template: JST['app/scripts/templates/urlrequest.ejs'],

        className: 'urlrequest',

        events: {
            'click #button-add': 'addEmpty',
            'click #button-clear': 'clearResponse',
            'click .alert button': 'hideAlert'
        },

        initialize: function () {
            this.params = new KeyValueListView({collection: new KeyValueCollection()});
            this.headers = new KeyValueListView({collection: new KeyValueCollection()});
        },

        render: function() {
            this.$el.html( this.template() );
            this.$('#parameters').append( this.params.render().el );
            this.$('#headers').append( this.headers.render().el );
            return this;
        },

        addEmpty: function() {
            if (this.params.$el.is(':visible')) {
                this.params.collection.add(new KeyValueModel());
            } else {
                this.headers.collection.add(new KeyValueModel());
            }
        },

        setUrl: function(url, allowEmpty) {
            var protocol = url.attr('protocol') || 'http',
                host = url.attr('host') || '',
                path = url.attr('path') || '';
            this.$('select[name="protocol"]').val(protocol);
            if (host) {
                var port = url.attr('port');
                if (port) {
                    this.$('input[name="host"]').val(host + ':' + port);
                } else {
                    this.$('input[name="host"]').val(host);
                }
            }
            if (path) {
                this.$('input[name="path"]').val(path);
            }
            this.params.collection.reset();
            _.each(_.pairs(url.param()).sort(), function(t) {
                if (!allowEmpty && t[1] === '') {
                    return;
                }
                this.params.collection.add(new KeyValueModel({key: t[0], value: t[1]}));
            }, this);
        },

        getUrl: function() {
            var protocol = this.$('select[name="protocol"]').val(),
                host = this.$('input[name="host"]').val(),
                path = this.$('input[name="path"]').val(),
                params = this.params.collection.toNVPairs();
            if (protocol === '' || host === '') {
                return;
            }
            return protocol + '://' + host + (path || '/') +
                   (_.isEmpty(params) ? '' : ('?' + $.param(params)));
        },

        send: function() {
            if (!this.$('input[name="host"]').val()) {
                this.$('.alert p').text('domain or host is not defined');
                this.$('.alert').show();
                return;
            }
            var self = this,
                url = this.getUrl();
            self.response = null;
            $.ajax({
                type: 'GET',
                dataType: 'text',  // TODO: Set from user-interface
                url: url,
                headers: this.headers.collection.toNVPairs()
            }).done(function( data ) {
                self.$('#response').text(data);
            }).fail(function( err ) {
                if (console && console.error) {
                    console.error( err );
                }
                self.$('#response').text('Fail to load: ' + url);
            }).always(function() {
            });
        },

        clearResponse: function() {
            this.$('#response').text('');
        },

        hideAlert: function() {
            this.$('.alert').hide();
        }
    });

    return UrlRequestView;
});
