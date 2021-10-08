$('.panel').on('show', function(event) {
    $(this).addClass('panel-show');

    var widgetIds = $(this).find('.widget').map(function() {
        return this.id;
    }).get();

    $('.app').trigger('register-widgets', [widgetIds]);
        
});
$('.panel').on('hide', function(event) {
    $(this).removeClass('panel-show');
});
