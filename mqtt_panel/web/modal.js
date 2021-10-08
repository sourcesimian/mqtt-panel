class Modal {
    constructor() {
        var This = this;
        $('#modal').on('confirm', function(event, blob) {
            This.on_confirm(blob);
        });
    }

    on_confirm(blob) {
        var window = $('<div></div>')
        var close = $('<span id="modal-close" class="material-icons" style="float:right;">close</span>');
        var panel = $('<div></div>')
        window.append(close);
        window.append(panel);

        panel.append($('<div id="modal-message">' + blob.message + '</div>'));
        
        var buttons = $('<div id="modal-buttons"></div>');

        var timeout = null;
        if (blob.timeout) {
            timeout = setTimeout(function() {
                $('#modal').addClass('d-none');
                blob.decline();
            }, blob.timeout);
        }
        
        var yes = $('<div><button>Yes</button></div>')
        $(yes).click(function() {
            $('#modal').addClass('d-none');
            clearTimeout(timeout);
            blob.proceed();
        });
        buttons.append(yes);

        buttons.append($('<div style="width:30px"></div>'));

        var no = $('<div><button>No</button></div>')
        buttons.append(no);

        var decline = function() {
            $('#modal').addClass('d-none');
            clearTimeout(timeout);
            blob.decline();
        };

        $('#modal').click(decline);
        $(window).click(function(event) {
            event.stopPropagation();
        });
        $(close).click(decline);
        $(no).click(decline);
        
        panel.append(buttons);
        $('#modal').html(window);
        $('#modal').removeClass('d-none');
    }
}
