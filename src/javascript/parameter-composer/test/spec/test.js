/*global define, describe, it */
define(function(require) {
    'use strict';
    var KeyValueModel = require('models/keyvalue-model'),
        KeyValueCollection = require('collections/keyvalue-collection'),
        CriteriaView = require('views/criteria-view'),
        DialogView = require('views/dialog-view'),
        FooterView = require('views/footer-view'),
        HeaderView = require('views/header-view'),
        KeyValueListView = require('views/keyvalue-list-view'),
        KeyValueView = require('views/keyvalue-view'),
        MainView = require('views/main-view'),
        UrlRequestView = require('views/urlrequest-view');

    describe('KeyValueModel', function() {

        describe('Default Value', function() {
            it('should have default values as empty', function() {
                var sample = new KeyValueModel();
                sample.get('key').should.equal('');
                sample.get('value').should.equal('');
            });
            it('should have keys on JSON', function() {
                var attrs = new KeyValueModel().toJSON();
                attrs.should.have.property('key', '');
                attrs.should.have.property('value', '');
            });
        });

    });

    describe('CriteriaView', function() {

        describe('Initialize', function() {
            it('does nothing', function() {
                var view = new CriteriaView();
                view.should.not.have.property('model');
            });
        });

    });

    describe('DialogView', function() {

        describe('Initialize', function() {
            it('does nothing', function() {
                var view = new DialogView();
                view.should.not.have.property('model');
            });
        });

    });

    describe('FooterView', function() {

        describe('Initialize', function() {
            it('does nothing', function() {
                var view = new FooterView();
                view.should.not.have.property('model');
            });
        });

    });

    describe('HeaderView', function() {

        describe('Initialize', function() {
            it('does nothing', function() {
                var view = new HeaderView();
                view.should.not.have.property('model');
            });
        });

    });

    describe('KeyValueListView', function() {

        describe('Initialize', function() {
            it('should have internal collection', function() {
                var view = new KeyValueListView({collection: new KeyValueCollection()});
                view.should.have.property('collection');
            });
        });

    });

    describe('KeyValueView', function() {

        describe('Initialize', function() {
            it('should have internal model', function() {
                var view = new KeyValueView({model: new KeyValueModel()});
                view.should.have.property('model');
                view.model.get('key').should.equal('');
                view.model.get('value').should.equal('');
            });
        });

    });

    describe('MainView', function() {

        describe('Initialize', function() {
            it('should have sub views', function() {
                var view = new MainView();
                view.should.have.property('header');
                view.should.have.property('footer');
                view.should.have.property('criteria');
                view.should.have.property('request');
                view.should.have.property('dialog');
            });
        });

    });

    describe('UrlRequestView', function() {

        describe('Initialize', function() {
            it('should have sub views', function() {
                var view = new UrlRequestView();
                view.should.have.property('params');
                view.should.have.property('headers');
            });
        });

    });

});
