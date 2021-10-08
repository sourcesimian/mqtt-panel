$(function() {
    $('.widget-image').on('update', function(event, blob) {
        $(this).data('mtime', blob.mtime);
        $(this).find('img').attr('src', blob.url)
        $(this).trigger('enable');
    });
});
