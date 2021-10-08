$(function() {
    $('.widget-dropdown').on('update', function(event, blob) {
        $(this).data('mtime', blob.mtime);
        $(this).find('button').text(blob.value);
        $(this).trigger('enable');
    });

    $('.widget-dropdown').on('offline', function(event) {
        $(this).find('button').prop('disabled', true);
    });

    $('.widget-dropdown').on('online', function(event) {
        $(this).find('button').prop('disabled', false);
    });

});

function on_widget_dropdown(id, value) {
    $('.app').trigger('widget', {
        id: id,
        value: value,
    });
}    
