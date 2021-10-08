class LinkOverlay {
    constructor(retry) {
        this.retry = retry;

        var This = this;
        $('#link-overlay-alert').click(function(event) {
            This.on_retry();
        });
    }

    on_retry() {
        this.retry();
    }

    show(message) {
      $('#link-overlay-alert').html(message);
      $('#link-overlay').removeClass('d-none');
      $('#link-overlay-alert').removeClass('d-none');
    }

    hide() {
      $('#link-overlay').addClass('d-none');
      $('#link-overlay-alert').addClass('d-none');
    }

    update(serverOnline, mqttOnline) {
        if (serverOnline && mqttOnline) {
            $('#link-overlay').addClass('d-none');
            $('#link-overlay-alert').addClass('d-none');
        } else {
            $('#link-overlay').removeClass('d-none');
            $('#link-overlay-alert').removeClass('d-none');
        }
        if (!mqttOnline) {
            $('#link-overlay-alert').html('MQTT server offline');
        }
    }

    countdown(countdown) {
        var span = $('<span> Link down</span>');
        span.prepend($('<span class="material-icons">cloud_off</span>'));
        if (countdown > 1) {
            span.append(navigator.onLine ? '' : '(you are offline)');
            span.append(' ... retry in ' + countdown + 's (tap to retry now)');
        } else {
            span.append(' ... retrying now');
        }
        $('#link-overlay-alert').html(span);
    }
}
