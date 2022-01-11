$(function() {
    $('.widget-iframe').on('update', function(event, blob) {
        $(this).data('mtime', blob.mtime);
        let src_change = $(this).find('iframe').attr('src') != blob.src
        $(this).find('iframe').attr('src', blob.src)

        $(this).trigger('enable');

        if (this.interval) {
            if (src_change == false) {
                return;
            }
            clearInterval(this.interval);
            this.interval = null;
        }
        let iframe = $(this).find('iframe');
        let refresh = parseInt($(iframe).data('refresh'));

        if (refresh) {
            this.interval = setInterval(function() {
                $(iframe).attr('src', function(_, val) {
                    return val;
                });
            }, refresh * 1000);
        }
    });

    $('.widget-iframe').on('disable', function(event, blob) {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
    });
});
