/*global require,L*/
'use strict';

require.config({
    shim: {
        underscore: {
            exports: '_'
        },
        backbone: {
            deps: [
                'underscore',
                'jquery'
            ],
            exports: 'Backbone'
        },
        bootstrap: {
            deps: ['jquery'],
            exports: 'jquery'
        }
    },
    paths: {
        jquery: '../bower_components/jquery/jquery',
        backbone: '../bower_components/backbone/backbone',
        underscore: '../bower_components/underscore/underscore',
        bootstrap: 'vendor/bootstrap'
    }
});

require([
    'jquery',
    'backbone',
    'routes/application',
    'views/point',
    'views/about',
    'models/point',
    'models/jpgrid'
], function ($, Backbone, ApplicationRouter, PointView, AboutView, PointModel, JpGridModel) {

    var SERVER_END_POIINT = 'http://localhost:10084/',
        DEFAULT_GRID = 'base',
        DEFAULT_CENTER = [35.680899, 139.767165],
        DEFAULT_ZOOM = 13,
        APPLICATION_ID = 'skitazaki.hm59ichp';

    Backbone.history.start();
    var router = new ApplicationRouter(),
        currentGrid = DEFAULT_GRID,
        map = L.mapbox.map('map', APPLICATION_ID).setView(DEFAULT_CENTER, DEFAULT_ZOOM),
        objects = [];

    var model = new PointModel({urlRoot: SERVER_END_POIINT}),
        jpgrid = new JpGridModel({urlRoot: SERVER_END_POIINT}),
        view = new PointView({el: '#sidebar', model: model});

    function showCoordinates(e) {
        model.set('lat', e.latlng.lat);
        model.set('lng', e.latlng.lng);
        model.fetch();
    }
    map.on('click', showCoordinates);

    function showGridLine(e) {
        var o = L.geoJson(e.toJSON());
        o.addTo(map);
        objects.push(o);
    }

    model.on('change:grid', function(e) {
        jpgrid.set('grid', e.get('grid')[currentGrid]);
        jpgrid.fetch();
    });
    jpgrid.on('change:geometry', showGridLine);

    router.on('route:clear', function() {
        $.each(objects, function(i, o) {
            map.removeLayer(o);
        });
        objects = [];
        router.navigate('/', {trigger: true, replace: true});
    });

    view.setGridLevel(currentGrid);
    router.on('route:grid', function(grid) {
        currentGrid = grid;
        view.setGridLevel(currentGrid);
        $('#grid-select li').removeClass('active');
        $('#grid-select a[href="#grid/' + grid + '"]').parent().addClass('active');
    });

    var v = new AboutView();
    $('.footer').append(v.$el);
    router.on('route:about', function() {
        v.show();
        router.navigate('/', {trigger: true, replace: true});
    });
});

