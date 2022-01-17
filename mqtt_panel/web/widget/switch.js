$(function() {
    $('.widget-switch').on('update', function(event, blob) {
        $(this).data('mtime', blob.mtime);
        $(this).data('value', blob.value);

        $(this).find('.value-item').addClass('d-none');
        $(this).find('.value-' + blob.value).removeClass('d-none');

        $(this).trigger('enable');
        $(this).trigger('release');
    });

    $('.widget-switch').click(function() {
        if ($(this).data('enable') == false) { return; }

        if ($(this).data('pending') == true) {
            $(this).trigger('release');
            return;
        }
        var value = $(this).data('value');
        value = $(this).find('.value-' + value).data('next');
        if (value === undefined) {
            $(this).trigger('release');
            return;
        }

        var This = this;

        var send = function() {
            $(This).data('pending', true);
            $('#app').trigger('widget', {
                id: $(This).data('id'),
                value: value,
            });
        };

        var confirm = $(this).find('.value-' + value).data('confirm');
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

    $('.widget-switch').each(function() {
        widget_clickable(this);
    });
});
