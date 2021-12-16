$(function() {
    $('.widget-gauge').on('update', function(event, blob) {
        $(this).data('mtime', blob.mtime);

        $(this).find('div div span').css('height', blob.percent + '%');
        $(this).find('div div span').css('background-color', blob.color);
        $(this).find('.text').text(blob.text);
        $(this).find('.value').text(blob.value);
        $(this).find('.material-icons').text(blob.icon);

        $(this).trigger('enable');
    });
});
