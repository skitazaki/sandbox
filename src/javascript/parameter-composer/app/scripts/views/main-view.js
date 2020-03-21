/*global define*/

define([
    'jquery',
    'underscore',
    'backbone',
    'templates',
    'views/header-view',
    'views/footer-view',
    'views/criteria-view',
    'views/dialog-view',
    'views/urlrequest-view'
], function ($, _, Backbone, JST, HeaderView, FooterView, CriteriaView, DialogView, UrlRequestView) {
    'use strict';

    var MainView = Backbone.View.extend({

        template: JST['app/scripts/templates/main.ejs'],

        events: {
        },

        initialize: function () {
            this.header = new HeaderView( {el: this.options.header} );
            this.footer = new FooterView( {el: this.options.footer} );
            this.criteria = new CriteriaView();
            this.request = new UrlRequestView();
            this.dialog = new DialogView();
            this.listenTo( this.header, 'toggleCriteria', this.toggleCriteria );
            this.listenTo( this.header, 'showDialog', this.showDialog );
            this.listenTo( this.footer, 'showDialog', this.showDialog );
            this.request.listenTo(this.criteria, 'parsed', this.request.setUrl);
            this.request.listenTo(this.footer, 'sendRequest', this.request.send);
        },

        render: function() {
            this.$el.html( this.template() );
            this.$('.row:first').append( this.criteria.render().el );
            this.$('.row:nth-child(2)').append( this.request.render().el );
            this.$el.append( this.dialog.render().el );
            this.header.render();
            this.footer.render();
            return this;
        },

        toggleCriteria: function() {
            this.criteria.$el.toggle('slow');
        },

        showDialog: function(type) {
            var options = {};
            var url = this.request.getUrl();
            if (type === 'bookmarklet') {
                var selfUrl = window.location.origin + window.location.pathname;
                options.title = 'Bookmarklet';
                options.text = 'javascript:(function() {' +
                        'window.open("' + selfUrl + '?" + ' + 'window.location.href); })()';
            } else if (type === 'json') {
                options.title = 'Parameters as JSON';
                var params = this.request.params.collection.toNVPairs();
                options.text = params ? JSON.stringify(params, null, 2) : 'No parameters';
            } else if (type === 'url') {
                options.title = 'Composed URL';
                if (url) {
                    options.url = url;
                } else {
                    options.text = 'No URL is given';
                }
            } else if (type === 'curl') {
                options.title = 'cURL command';
                var headers = this.request.headers.collection.toNVPairs();
                options.text = '$ curl "' + url + '"';
                if (!_.isEmpty(headers)) {
                    _.each(headers, function(v, k) {
                        options.text += ' -H "' + k + '=' + v + '"';
                    });

                }
            }
            this.dialog.show(options);
        }
    });

    return MainView;
});
