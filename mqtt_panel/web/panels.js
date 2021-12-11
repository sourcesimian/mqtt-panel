$('.panel').on('show', function(event) {
    $('.panel').trigger('hide');
    $(this).addClass('panel-show');

    var widgetIds = $(this).find('.widget').map(function() {
        return $(this).data('id');
    }).get();

    $('.app').trigger('register-widgets', [widgetIds]);
        
});
$('.panel').on('hide', function(event) {
    $(this).removeClass('panel-show');
});
