$(function() {
    $('.widget-button').on('update', function(event, blob) {
        $(this).data('mtime', blob.mtime);

        $(this).trigger('enable');
        $(this).trigger('release');
    });

    $('.widget-button').click(function() {
        if ($(this).data('enable') == false) { return; }

        if ($(this).data('pressed') == true) {
            $(this).trigger('release');
            return;
        }

        var This = this;

        var send = function() {
            $('#app').trigger('widget', {
                id: $(This).data('id'),
            });
            $(This).data('pressed', true);
        };

        var confirm = $(this).find('.value').data('confirm');
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

    $('.widget-button').mousedown(function() {
        if ($(this).data('enable') == false) { return; }

        $(this).addClass('widget-press');
        $(this).find('*').addClass('widget-press');
    });

    $('.widget-button').on('release', function() {
        $(this).removeClass('widget-press');
        $(this).find('*').removeClass('widget-press');
        $(this).data('pressed', false);
    });
});
