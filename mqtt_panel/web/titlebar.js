class TitleBar {
    constructor() {
        var This = this;
        $('.titlebar-toggle-menubar').click(function() {
            $('.menubar').trigger('toggle');
        });
    }

    title(str) {
        $('.titlebar-title').html(str);
    }
}
