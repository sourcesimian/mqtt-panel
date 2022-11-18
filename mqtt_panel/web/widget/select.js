$(function() {
    $('.widget-select').on('update', function(event, blob) {
        $(this).data('mtime', blob.mtime);
        $(this).data('value', blob.value);

        $(this).find('.value-item').addClass('d-none');
        $(this).find('.value-' + blob.value).removeClass('d-none');

        $(this).trigger('enable');
        $(this).trigger('release');
    });

    $('.widget-select').click(function() {
        if ($(this).data('enable') == false) { return; }

        if ($(this).data('pending') == true) {
            $(this).trigger('release');
            return;
        }

        let This = this;

        let buttons = [];
        $(this).find('.value-item').map(function() {
            let name = $(this).data('name');
            let ro = $(this).data('ro');
            if  (name != null && ro == false) {
                let button = {
                    icon: $(this).data('icon'),
                    color: $(this).data('color'),
                    text: $(this).data('text'),
                    confirm: $(this).data('confirm'),
                    click: function() {
                        $(This).data('pending', true);
                        $('#app').trigger('widget', {
                            id: $(This).data('id'),
                            value: name,
                        });
                    },
                };
                buttons.push(button);
            }
        });

        widget_select_modal({
            message: $(this).find('.title').text(),
            timeout: null,
            cancel: function () {
                $(This).trigger('release');
            },
            buttons: buttons,
        });
    })

    $('.widget-select').each(function() {
        widget_clickable(this);
    });
});

function widget_select_modal(blob) {
    let window = $('<div></div>')
    let close = $('<span class="modal-close material-icons">close</span>');
    let panel = $('<div></div>')
    window.append(close);
    window.append(panel);

    panel.append($('<div class="modal-message">' + blob.message + '</div>'));

    let buttons = $('<div class="modal-select"></div>');

    for (let i in blob.buttons) {
        let button = blob.buttons[i];
        let icon = '';
        if (button.icon !== undefined) {
            icon = button.icon;
        }
        let color = '';
        if (button.color !== undefined) {
            color = ' style="color:' + button.color + '"';
        }
        let html = $('<div></div>')
        html.append($('<span class="material-icons"' + color + '>' + icon + '</span>'));
        html.append($('<span' + color + '> ' + button.text + '</span>'));
        let click = function() {
            $('#modal').trigger('close');
            button.click();
        }
        if (button.confirm) {
            $(html).click(function(event) {
                event.stopPropagation();
                $('#modal').trigger('close');
                $('#modal').trigger('confirm', [{
                    message: button.confirm,
                    proceed: click,
                    cancel: blob.cancel,
                    timeout: 7000,
                }]);
            });
        } else {
            $(html).click(function(event) {
                event.stopPropagation();
                click();
            });
        }

        buttons.append(html);
    }

    $(window).click(function(event) {
        event.stopPropagation();
    });
    $(close).click(function() {
        $('#modal').trigger('cancel');
    });

    panel.append(buttons);

    $('#modal').trigger('show', [window, blob.cancel, blob.timeout]);
}
