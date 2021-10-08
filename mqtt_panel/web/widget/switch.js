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

        if ($(this).data('pressed') == true) {
            $(this).trigger('release');
            return;
        }
        var value = $(this).data('value');
        value = $(this).find('.value-' + value).data('next');
        if (!value) {
            $(this).removeClass('widget-press');
            $(this).find('*').removeClass('widget-press');
            return;
        }

        var This = this;

        var send = function() {
            $('.app').trigger('widget', {
                id: $(This).data('id'),
                value: value,
            });
            $(This).data('pressed', true);
        };

        var confirm = $(this).find('.value-' + value).data('confirm');
        if (confirm) {
            var decline = function () {
                $(This).trigger('release');
            };
    
            $('#modal').trigger('confirm', [{
                message: confirm,
                proceed: send,
                decline: decline,
                timeout: 7000,
            }]);
        } else {
            send();
        }
    });

    $('.widget-switch').mousedown(function() {
        if ($(this).data('enable') == false) { return; }

        $(this).addClass('widget-press');
        $(this).find('*').addClass('widget-press');
    });

    $('.widget-switch').on('release', function() {
        $(this).removeClass('widget-press');
        $(this).find('*').removeClass('widget-press');
        $(this).data('pressed', false);
    });
});
