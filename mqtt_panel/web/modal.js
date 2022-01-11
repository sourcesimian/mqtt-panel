class Modal {
    constructor() {
        var This = this;
        $('#modal').on('confirm', function(event, blob) {
            This.on_confirm(blob);
        });
        document.addEventListener('keydown', function(event){
            if(event.key === "Escape"){
                $('#modal').find('.modal-close').click();
            }
        });

        $('#modal').click(function() {
            This.cancel();
        });

        this.on_cancel = null;
        this.cancel_timeout = null;

        $('#modal').on('close', function(event, blob) {
            This.close(blob);
        });
        $('#modal').on('cancel', function(event, blob) {
            This.cancel(blob);
        });
        $('#modal').on('show', function(event, html, on_cancel, timeout) {
            This.show(html, on_cancel, timeout);
        });
    }

    close() {
        $('#modal').addClass('d-none');
        $('#modal').empty();
        if (this.cancel_timeout) {
            clearTimeout(this.cancel_timeout);
            this.cancel_timeout = null;
        }
    }

    cancel() {
        this.close();
        if (this.on_cancel) {
            this.on_cancel();
        }
    }

    show(html, on_cancel, timeout) {
        this.on_cancel = on_cancel;
        let This = this;
        if (timeout) {
            this.cancel_timeout = setTimeout(function() {
                    This.cancel();
                }, timeout);
        }
        $('#modal').empty();
        $('#modal').html(html);
        $('#modal').removeClass('d-none');
    }

    on_confirm(blob) {
        let window = $('<div></div>')
        let close = $('<span class="modal-close material-icons">close</span>');
        let panel = $('<div></div>')
        window.append(close);
        window.append(panel);

        panel.append($('<div class="modal-message">' + blob.message + '</div>'));

        let buttons = $('<div class="modal-buttons"></div>');

        let yes = $('<div><button>Yes</button></div>')
        $(yes).click(function() {
            $('#modal').trigger('close');
            blob.proceed();
        });
        buttons.append(yes);

        buttons.append($('<div style="width:30px"></div>'));

        let no = $('<div><button>No</button></div>')
        buttons.append(no);

        $(window).click(function(event) {
            event.stopPropagation();
        });
        $(close).click(function() {
            $('#modal').trigger('cancel');
        });
        $(no).click(function() {
            $('#modal').trigger('cancel');
        });
        
        panel.append(buttons);

        $("#modal").trigger('show', [window, blob.cancel, blob.timeout]);
    }
}
