/*global define*/

define([
    'underscore',
    'backbone',
    'models/jpgrid'
], function (_, Backbone, JpGridModel) {
    'use strict';

    var JpGridCollection = Backbone.Collection.extend({
        model: JpGridModel
    });

    return JpGridCollection;
});
