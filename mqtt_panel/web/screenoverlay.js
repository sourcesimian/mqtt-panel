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
    }

    alert(message) {
        $('#screen-overlay').removeClass('d-none');
        $('#screen-overlay .alert').removeClass('d-none');
        $('#screen-overlay .alert').html(message);
        if (onclick !== undefined) {
            $('#screen-overlay .alert').on('click', onclick);
        } else {
            $('#screen-overlay .alert').off('click');
        }
    }

    spinner() {
        $('#screen-overlay').removeClass('d-none');
        $('#screen-overlay .spinner').removeClass('d-none');
    }    

    hide() {
        $('#screen-overlay').addClass('d-none');
        $('#screen-overlay .alert').addClass('d-none');
        $('#screen-overlay .alert').off('click');
        $('#screen-overlay .spinner').addClass('d-none');
    }
}
