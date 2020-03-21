/*global define*/

define([
    'underscore',
    'backbone',
    'models/keyvalue-model'
], function (_, Backbone, KeyValueModel) {
    'use strict';

    var KeyValueCollection = Backbone.Collection.extend({

        model: KeyValueModel,

        toNVPairs: function() {
            if (this.size() === 0) { return; }
            var nvp = {};
            this.each(function(p) {
                if (p.get('key')) {
                    nvp[p.get('key')] = p.get('value');
                }
            });
            return nvp;
        }

    });

    return KeyValueCollection;
});
