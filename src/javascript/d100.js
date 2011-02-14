/**
 * OData sample.
 */
function load_odata(url, screen) {
    $.template('template', "<li>${Name} (<a href='${Link}'>get</a>)</li>");

    OData.read(url, function (data) {
        console.log(data);
        var dt = [];
        for (num in data.results) {
            var entry = data.results[num];
            dt.push({Name: entry.Name, Link: entry.Titles.__deferred.uri});
        }
        screen.empty();
        $.tmpl('template', dt).appendTo(screen);
    });
}

$(function() {
    $('form').submit(function() {
        try {
            load_odata($(this).find('input[name=url]').val(), $('#contents'));
        } catch (e) {
            console.log(e);
        }
        return false;
    });

    $('#contents a').live('click', function() {
        load_odata($(this).attr('href'), $('#contents'));
        return false;
    });
});

