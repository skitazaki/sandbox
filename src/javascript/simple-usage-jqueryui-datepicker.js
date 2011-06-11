$(function() {
    $('input.date').datepicker({dateFormat: 'yy/mm/dd'});
    $('#main form').submit(function() {
        var val = $(this).find('input[name=date]').val();
        if (val)
            $('<li/>').text(val).appendTo('#contents');
        return false;
    });
});

