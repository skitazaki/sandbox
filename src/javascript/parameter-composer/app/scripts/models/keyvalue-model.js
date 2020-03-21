/*global define*/

define([
    'underscore',
    'backbone'
], function (_, Backbone) {
    'use strict';

    var KeyValueModel = Backbone.Model.extend({
        defaults: {
            key: '',
            value: ''
        }
    });

    return KeyValueModel;
});
