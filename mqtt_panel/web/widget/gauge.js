$(function() {
    $('.widget-gauge').on('update', function(event, blob) {
        $(this).data('mtime', blob.mtime);

        widget_gauge_update(this, blob);
    });
});

function widget_gauge_range_meta(ranges, value) {
    let meta;
    match: {
        if (value != null) {
            for (i in ranges.ranges) {
                let range = ranges.ranges[i];
                if (range.start <= value && value <= range.end) {
                    meta = range;
                    break match;
                }
            }
        }
        meta = ranges;
    }
    meta.percent = 0;
    if (value != null) {
        if (ranges.min <= value && value <= ranges.max) {
            meta.percent = (value - ranges.min) / (ranges.max - ranges.min) * 100;
        }
    }
    return meta;
}

function widget_gauge_update(This, blob) {
    $(This).find('.value').data('value', blob.value);
    $(This).find('.value').text(blob.value != null ? blob.value : '?');

    let ranges = $(This).find('.value').data('ranges');
    let meta = widget_gauge_range_meta(ranges, blob.value)

    $(This).find('div div span').css('background-color', meta.color);
    $(This).find('.text').text(meta.text);
    $(This).find('.material-icons').text(meta.icon);
    $(This).find('div div span').css('height', meta.percent + '%');

    $(This).trigger('enable');
};
