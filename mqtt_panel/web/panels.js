$('.panel').on('show', function(event) {
    $('.panel').trigger('hide');
    $(this).removeClass('d-none');
    $(this).addClass('panel-active');

    var widgetIds = $(this).find('.widget').map(function() {
        return $(this).data('id');
    }).get();

    $('#app').trigger('register-widgets', [widgetIds]);
        
});
$('.panel').on('hide', function(event) {
    $(this).addClass('d-none');
    $(this).removeClass('panel-active');
});
