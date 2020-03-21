/*global require*/
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
        },
        ecljs: {
            exports: 'ECL',
            init: function() {
                var ECL = {};
                // List is "http://www.junoe.jp/downloads/itoh/enc_js.shtml"
                /*global EscapeSJIS, UnescapeSJIS */
                ECL.EscapeSJIS = EscapeSJIS;
                ECL.UnescapeSJIS = UnescapeSJIS;
                /*global EscapeEUCJP, UnescapeEUCJP */
                ECL.EscapeEUCJP = EscapeEUCJP;
                ECL.UnescapeEUCJP = UnescapeEUCJP;
                /*global EscapeJIS7, UnescapeJIS7 */
                ECL.EscapeJIS7 = EscapeJIS7;
                ECL.UnescapeJIS7 = UnescapeJIS7;
                /*global EscapeJIS8, UnescapeJIS8 */
                ECL.EscapeJIS8 = EscapeJIS8;
                ECL.UnescapeJIS8 = UnescapeJIS8;
                /*global EscapeUnicode, UnescapeUnicode */
                ECL.EscapeUnicode = EscapeUnicode;
                ECL.UnescapeUnicode = UnescapeUnicode;
                /*global EscapeUTF7, UnescapeUTF7 */
                ECL.EscapeUTF7 = EscapeUTF7;
                ECL.UnescapeUTF7 = UnescapeUTF7;
                /*global EscapeUTF8, UnescapeUTF8 */
                ECL.EscapeUTF8 = EscapeUTF8;
                ECL.UnescapeUTF8 = UnescapeUTF8;
                /*global EscapeUTF16LE, UnescapeUTF16LE */
                ECL.EscapeUTF16LE = EscapeUTF16LE;
                ECL.UnescapeUTF16LE = UnescapeUTF16LE;
                /*global GetEscapeCodeType, JCT11280, JCT8836 */
                ECL.GetEscapeCodeType = GetEscapeCodeType;
                ECL.JCT11280 = JCT11280;
                ECL.JCT8836 = JCT8836;
                return ECL;
            }
        }
    },
    paths: {
        jquery: '../bower_components/jquery/jquery',
        backbone: '../bower_components/backbone-amd/backbone',
        underscore: '../bower_components/underscore-amd/underscore',
        purl: '../bower_components/purl/purl',
        bootstrap: 'vendor/bootstrap',
        ecljs: 'vendor/ecl'
    }
});

require([
    'backbone',
    'purl',
    'routes/main-router',
    'views/main-view',
    'bootstrap'
], function (Backbone, purl, Router, MainView) {
    Backbone.history.start();
    new Router();

    var app = new MainView( {el: '#main', header: '#header', footer: '#footer'} );
    app.render();

    // Activate Bootstrap tab layout
    $('#params-headers a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    });

    var q = window.location.search || '';
    if (q.length > 1) {  // begin with '?' character
        var url = purl(q.substring(1));
        app.request.setUrl(url, true);  // true to allow empty value pair
    }

});

