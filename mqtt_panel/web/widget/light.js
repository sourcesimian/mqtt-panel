$(function() {
    $('.widget-light').on('update', function(event, blob) {
        $(this).data('mtime', blob.mtime);
        $(this).data('value', blob.value);

        $(this).find('.value-item').addClass('d-none');
        $(this).find('.value-' + blob.value).removeClass('d-none');

        $(this).trigger('enable');
    });
});
