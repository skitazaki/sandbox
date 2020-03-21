$(function(){
    $("#account").submit(function() {
        var $form = $(this),
            $message = $('#message');
        $form.find('input[name=username],input[name=password]')
             .each(function() {
            var $field = $(this);
            if (!$field.val().length) {
                $message.text("Please fill in the form.");
                $field.addClass('error');
                setTimeout(function() {
                    $message.empty();
                    $field.removeClass('error');
                }, 3000);
            }
        });
        if ($message.text()) {
            return false;
        }
        $form.find('input[type=submit]').attr('disabled', true);
        $.ajax({
            type: $form.attr('method'),
            url: $form.attr('action') || '',
            cache: false,
            data: $form.serialize(),
            dataType: 'text',
            success: function(data) {
                if (data.indexOf('http') === 0) {
                    $message.text("Moving: " + data);
                    setTimeout(function() {
                        location.href = data;
                    }, 2000);
                }
                $form.fadeOut('slow');
                $message.text(data);
            },
            error: function(xhr) {
                $form.find('input[type=submit]').attr('disabled', false);
                $message.text(xhr.responseText);
                setTimeout(function() {
                    $message.empty();
                }, 3000);
            }
        });
        return false;
    });
});

