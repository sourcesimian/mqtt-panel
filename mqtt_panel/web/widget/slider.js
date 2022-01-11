$(function() {
    $('.widget-slider').on('update', function(event, blob) {
        $(this).data('mtime', blob.mtime);

        widget_gauge_update(this, blob);

        $(this).trigger('enable');
        $(this).trigger('release');

        $('#modal .modal-slider-' + blob.id).trigger('update', blob.value);
    });

    $('.widget-slider').click(function() {
        if ($(this).data('enable') == false) { return; }

        if ($(this).data('pressed') == true) {
            $(this).trigger('release');
            return;
        }

        let change = null;
        if ($(this).find('.value').data('live') == 'True') {
            change = function(value) {
                if (This.live_timeout) {
                    This.live_value = value;
                } else {
                    This.live_timeout = setTimeout(function() {
                        if (This.live_value) {
                            $('#app').trigger('widget', {
                                id: $(This).data('id'),
                                value: This.live_value,
                            });
                        }
                        This.live_timeout = null;
                    }, 200);
                }
            }
        }

        let This = this;
        widget_slider_modal({
            message: $(this).find('.title').text(),
            timeout: null,
            change: change,
            done: function (value) {
                if (This.live_value != value) {
                    $('#app').trigger('widget', {
                        id: $(This).data('id'),
                        value: value,
                    });
                }
                This.live_value = null;
            },
            cancel: function () {
                $(This).trigger('release');
            },
            min: $(this).find('.value').data('min'),
            max: $(this).find('.value').data('max'),
            value: $(this).find('.value').data('value'),
            ranges: $(this).find('.value').data('ranges'),
            id: $(this).data('id'),
        });
    })

    $('.widget-slider').mousedown(function() {
        if ($(this).data('enable') == false) { return; }

        $(this).addClass('widget-press');
        $(this).find('*').addClass('widget-press');
    });

    $('.widget-slider').on('release', function() {
        $(this).removeClass('widget-press');
        $(this).find('*').removeClass('widget-press');
        $(this).data('pressed', false);
    });
});

function widget_slider_modal(blob) {
    let window = $('<div></div>')
    let close = $('<span class="modal-close material-icons">close</span>');
    let panel = $('<div></div>')
    window.append(close);
    window.append(panel);

    panel.append($('<div class="modal-message">' + blob.message + '</div>'));

    let slider = $('<div class="modal-slider modal-slider-' + blob.id + '"></div>');
    let icon_text = $('<div class="icon_text"></div>')
    let icon = $('<span class="icon material-icons"></span>');
    let text = $('<span class="text"></span>');
    icon_text.append(icon);
    icon_text.append(text);
    slider.append(icon_text);
    let value = $('<div class="value">' + (blob.value != null ? blob.value : '?') + '</div>');
    let max = $('<div class="max">' + blob.max + '</div>');
    let min = $('<div class="min">' + blob.min + '</div>');
    slider.append(value);
    slider.append(max);
    slider.append(min);
    let input = $('<input type="range" min="' + blob.min + '" max="' + blob.max + '" value="' + (blob.value != null ? blob.value : 0) + '" orient="vertical"></input>');
    slider.append(input);

    $(input).on('change', function (event) {
        $('#modal .modal-slider .value').text(event.target.value);
        $('#modal').trigger('close');
        blob.done(event.target.value)
    })

    function set_meta(_value) {
        let meta = widget_gauge_range_meta(blob.ranges, _value);
        $(icon).text(meta.icon);
        $(icon).css('color', meta.color);
        $(text).text(meta.text);
        $(text).css('color', meta.color);
        $(value).text((_value != null ? _value : '?'));
    }
    set_meta(blob.value);

    $(input).on('input change', function (event) {
        $('#modal .modal-slider').data('touched', true);
        if (blob.change) {
            blob.change(event.target.value);
        }
        set_meta(event.target.value);
    })

    $(slider).on('update', function(event, value){
        if (!$('#modal .modal-slider').data('touched')) {
            set_meta(value);
            $(input).attr('value', value);
        }
    });

    $(window).click(function(event) {
        event.stopPropagation();
    });
    $(close).click(function() {
        $('#modal').trigger('cancel');
    });

    panel.append(slider);

    $('#modal').trigger('show', [window, blob.cancel, blob.timeout]);
}
