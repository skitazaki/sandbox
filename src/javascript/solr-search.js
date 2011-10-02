/**
 * Simple Solr Console using jQuery and jQuery Template.
 *
 * CAUTION: This script does NOT analyze input keyword.
 *          Therefore, keyword which contains special symbols for Lucene
 *          may break server-side thread.
 *
 * `ajax-solr` is highly recommended.
 *
 * @see ajax-solr: http://evolvingweb.github.com/ajax-solr/
 */

var SOLR_SERVER_URL = 'http://example.com/solr/select';

(function($){
    $.solr = function(options) {
        var server = options.server || null,
            fields = options.fields || ['*', 'score'],
            logger = options.logger || $('#solr-logger');

        function log(msg) {
            if (!logger) return;
            if (logger.children().length > 10) {
                logger.children().first().remove();
            }
            logger.append($('<p></p>').text(msg));
        }

        function request(query, callback) {
            var param = {
                q  : query,
                fl : fields.join(','),
                wt : 'json'
            };
            $.getJSON(server + '?' + $.param(param), function(data) {
                log("NumFound: " + data.response.numFound);
                callback(data.response.docs);
            });
        }

        return {
            search : function(query, callback) {
                if (!query) {
                    return;
                }
                log("Query: " + query);
                request(query, callback);
            }
        };
    };
})(jQuery);

$(function() {
    var s = $.solr({server: SOLR_SERVER_URL, fields: ['id', 'name']}),
        $screen = $('#screen > tbody');

    $('form[action="search"]').submit(function(e) {
        e.preventDefault();
        s.search($('input[name=query]', this).val(), function(results) {
            var dt = [];
            $.each(results, function(i, doc) {
                //console.log(doc);
                dt.push({id: doc.id, name: doc.name});
            });
            $screen.fadeOut('fast', function() {
                $(this).empty()
                    .append($('#table-template').tmpl(dt))
                    .fadeIn('slow');
            });
        });
    });
});
