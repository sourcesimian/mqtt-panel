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

    $('.widget').on('release', function(event) {
        $(this).data('pending', false);
        $(this).data('pressed', false);

        $(this).removeClass('widget-press');
        $(this).find('*').removeClass('widget-press');
    });

    $('.widget').on('touched', function() {
        if ($(this).data('enable') == false) { return; }

        if ($(this).data('pressed') == true) {
            $(this).data('pending', true);
        } else {
            $(this).data('pressed', true);
        }

        $(this).addClass('widget-press');
        $(this).find('*').addClass('widget-press');
    });
});

function widget_clickable(This) {
    $(This).mousedown(function() {
        $(This).trigger('touched');
    });
    // $(This).touchstart(function() {
    //     $(This).trigger('touched');
    // });
    // $(This).mouseleave(function() {
    //     $(This).trigger('release');
    // });
}

function widget_update_last_update(This, now) {
    let mtime = $(This).data('mtime');
    let lastUpdate = '-';
    if (mtime){
        lastUpdate = widget_time_since(now, mtime);
    }
    $(This).find('.last-update').html(lastUpdate);
}

function widget_time_since(current, previous) {
    var msPerMinute = 60;
    var msPerHour = msPerMinute * 60;
    var msPerDay = msPerHour * 24;
    var msPerMonth = msPerDay * 30;
    var msPerYear = msPerDay * 365;
    var elapsed = current - previous;

    function roundToWords(elapsed, divisor, unit) {
        let value = Math.round(elapsed/divisor);
        if (value == 1) {
            return value + ' ' + unit + ' ago';
        }
        return value + ' ' + unit + 's ago';
    }

    if (elapsed < msPerHour) {
        return roundToWords(elapsed, msPerMinute, 'minute');
    }
    else if (elapsed < msPerDay ) {
        return roundToWords(elapsed, msPerHour, 'hour');
    }
    else if (elapsed < msPerMonth) {
        return roundToWords(elapsed, msPerDay, 'day');
    }
    else if (elapsed < msPerYear) {
        return roundToWords(elapsed, msPerMonth,'month');
    }
    else {
        return roundToWords(elapsed, msPerYear, 'year');
    }
}
