$(function() {
    $('.widget-value').on('update', function(event, blob) {
        $(this).data('mtime', blob.mtime);
        $(this).find('.value').text(blob.value)
        $(this).trigger('enable');
    });
});
