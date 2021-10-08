$(function() {
    $(".widget").on('enable', function(event) {
        $(this).data('enable', true);
        $(this).removeClass('widget-disable');
        $(this).find('*').removeClass('widget-disable');
    });

    $(".widget").on('disable', function(event) {
        $(this).data('enable', false);
        $(this).addClass('widget-disable');
        $(this).find('*').addClass('widget-disable');
    });
});
