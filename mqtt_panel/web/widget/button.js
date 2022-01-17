$(function() {
    $('.widget-button').on('update', function(event, blob) {
        $(this).data('mtime', blob.mtime);

        $(this).trigger('enable');
        $(this).trigger('release');
    });

    $('.widget-button').click(function() {
        if ($(this).data('enable') == false) { return; }

        if ($(this).data('pending') == true) {
            $(this).trigger('release');
            return;
        }

        var This = this;

        var send = function() {
            $(This).data('pending', true);
            $('#app').trigger('widget', {
                id: $(This).data('id'),
            });
        };

        var confirm = $(this).find('.value').data('confirm');
        if (confirm) {
            $('#modal').trigger('confirm', [{
                message: confirm,
                proceed: send,
                cancel: function () {
                    $(This).trigger('release');
                },
                timeout: 7000,
            }]);
        } else {
            send();
        }
    });

    $('.widget-button').each(function() {
        widget_clickable(this);
    });
});
