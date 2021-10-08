$(function() {
    $('.widget-text').on('update', function(event, blob) {
        $(this).data('mtime', blob.mtime);
        $(this).find('.text').text(blob.text);
        $(this).trigger('enable');
    });
});
