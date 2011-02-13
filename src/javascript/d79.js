/**
 * jQuery sample, the way to load the library and mouse event handling.
 * @ see <a href="http://api.jquery.com/hover/">.hover()</a>
 */
$(function() {
    $("a").each(function() {
        var h = $(this).attr("href"),
            t = $(this).text();

        if (!h && !t) {
            if ($(this).parent().text() || $(this).siblings().length)
                $(this).parent().remove($(this));
            else
                $(this).parent().remove();
        }
        else if (!h && t && t.indexOf("http") === 0)
            $(this).attr("href", t);
        else if (h && !t)
            $(this).text(h);

        if ($(this).text() !== $(this).attr("href")) {
            var link = $("<span></span>").hide().text($(this).attr("href"));
            $(this).parent().append($(link).css({margin:"5px", "font-size":"80%"}));
            $(this).hover(function() {
                link.toggle();
            });
        }
    });
});
