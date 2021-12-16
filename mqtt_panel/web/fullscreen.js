class FullScreen {
    constructor() {
        this.elem = document.documentElement;
        this.state = false;

        var This = this;
        $('#fullscreen').on('toggle', function(event) {
            This.toggle();
        });
    }

    toggle() {
        if (this.state) {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) { /* Safari */
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) { /* IE11 */
                document.msExitFullscreen();
            }
            this.state = false;
        } else {
            if (this.elem.requestFullscreen) {
                this.elem.requestFullscreen();
            } else if (this.elem.webkitRequestFullscreen) { /* Safari */
                this.elem.webkitRequestFullscreen();
            } else if (this.elem.msRequestFullscreen) { /* IE11 */
                this.elem.msRequestFullscreen();
            }
            this.state = true;
        }
    }
}
