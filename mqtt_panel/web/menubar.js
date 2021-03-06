class MenuBar {
    constructor(on_click) {
        this._on_click = on_click;

        var This = this;
        $('.menubar').on('toggle', function(event) {
            This.toggle();
        });

        $('.menubar').on('hide', function(event) {
            This.hide();
        });

        $('.menubar').click(function() {
            This.hide(this);
        });

        $('.menubar-overlay').click(function() {
            This.toggle(this);
        });

        $('.menubar-overlay').on('swiperight', function() {
            This.toggle(this);
        });

        $('.menubar-link').click(function(event) {
            var id = $(this).data('id');
            if (This._on_click(id)) {
                event.stopPropagation();
            }
        });
    }

    hide() {
        $('.menubar').removeClass('menubar-show');
        $('.menubar-overlay').addClass('d-none');
    }

    toggle() {
        $('.menubar').toggleClass('menubar-show');
        $('.menubar-overlay').toggleClass('d-none');
    }

    active(id) {
        $('.menubar-link').removeClass('active');
        $('.menubar-link[data-id="' + id + '"]').addClass('active');
    }
}
