$(function() {
    $('.widget-select').on('update', function(event, blob) {
        $(this).data('mtime', blob.mtime);
        $(this).find('select').val(blob.value);
        $(this).trigger('enable');
    });

    $('.widget-select').on('disable', function(event) {
        $(this).find('select').prop('disabled', true);
    });

    $('.widget-select').on('enable', function(event) {
        $(this).find('select').prop('disabled', false);
    });

    $('.widget-select select').change(function() {
        $('.app').trigger('widget', {
            id: $(this).data('id'),
            value: $(this).val(),
        });
    })

    $('.widget-select select').prop('disabled', true);
});
