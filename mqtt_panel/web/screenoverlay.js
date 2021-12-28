class ScreenOverlay {
    constructor() {
        var This = this;
        $('#screen-overlay').on('alert', function(event, message, onclick) {
            This.alert(message, onclick);
        });
        $('#screen-overlay').on('spinner', function(event) {
            This.spinner();
        });
        $('#screen-overlay').on('hide', function(event) {
            This.hide();
        });
        this.onclick = undefined;
        $('#screen-overlay .alert').on('click', function(event){
            if (This.onclick !== undefined) {
                This.onclick();
            }
            return false;
        });
    }

    alert(message, onclick) {
        $('#screen-overlay').removeClass('d-none');
        $('#screen-overlay .alert').removeClass('d-none');
        $('#screen-overlay .alert').html(message);
        this.onclick = onclick;
    }

    spinner() {
        $('#screen-overlay').removeClass('d-none');
        $('#screen-overlay .spinner').removeClass('d-none');
    }    

    hide() {
        $('#screen-overlay').addClass('d-none');
        $('#screen-overlay .alert').addClass('d-none');
        $('#screen-overlay .spinner').addClass('d-none');
    }
}
