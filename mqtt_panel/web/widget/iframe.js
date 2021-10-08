$(function() {
    $('.widget-iframe').on('update', function(event, blob) {
        $(this).data('mtime', blob.mtime);
        $(this).find('iframe').attr('src', blob.src)

        $(this).trigger('enable');
    });
});
