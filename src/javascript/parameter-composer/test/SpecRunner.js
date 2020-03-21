/*globals require */
require.config({
    baseUrl: '..',
    paths: {
        'jquery'      : 'app/bower_components/jquery/jquery',
        'underscore'  : 'app/bower_components/underscore-amd/underscore',
        'backbone'    : 'app/bower_components/backbone-amd/backbone',
        'purl'        : 'app/bower_components/purl/purl',
        'ecljs'         : 'app/scripts/vendor/ecl',
        'mocha'       : 'test/lib/mocha/mocha',
        'chai'        : 'test/lib/chai',
        'templates'   : '.tmp/scripts/templates',
        'models'      : 'app/scripts/models',
        'collections' : 'app/scripts/collections',
        'views'       : 'app/scripts/views'
    },
    shim: {
        'underscore': {
            exports: '_'
        },
        'jquery': {
            exports: '$'
        },
        'backbone': {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
        ecljs: {
            exports: 'ECL',
            init: function() {
                'use strict';
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
        },
        'mocha': {
            exports: 'mocha'
        }
    },
    urlArgs: 'v=' + (new Date()).getTime()
});

require(['require', 'chai', 'mocha'], function(require, chai, mocha) {
    'use strict';

    chai.should();
    mocha.setup('bdd');

    require([
        'spec/test.js'
    ], function() {
        mocha.run();
    });

});
