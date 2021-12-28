class WSLink {
    constructor(onmessage, online, offline, retry_countdown, path) {
        this.onmessage = onmessage;
        this.online = online;
        this.offline = offline;
        this.retry_countdown = retry_countdown;
        this.path = path;
        this._retry_max_delay = 60;
        this._retry_min_delay = 5;
        this._retry_countdown_init = this._retry_min_delay;
        this._retry_countdown = null;
        this.is_open = false;
    }

    close() {
        this._ws.close();
    }

    send(blob_list) {
      if (this.is_open == false) {
        return;
      }
      var msg = JSON.stringify(blob_list);
      console.log('WS Tx: ' + msg)
      this._ws.send(msg);
    }

    _url() {
        var port = (location.port === "") ? "" : ":" + location.port;
        var scheme = (location.protocol === "https:") ? "wss://" : "ws://";
        if (this.path.charAt(0) == '/') {
            /* Absolute path */
            var path = ''
        } else {
            /* Relative path */
            var path = location.pathname.substr(0, location.pathname.lastIndexOf('/'));
        }
        var url = scheme + document.domain + port + path + '/' + this.path;
        return url;
    }

    on_open() {
      this.is_open = true;
      this._retry_stop();
      this.online();
    }

    on_error() {
    }

    on_close() {
      this.is_open = false;
      this.offline();
      this._retry_start();
    }

    open() {
      var This = this;
      this._ws = new WebSocket( This._url() );
      this._ws.onopen = function(event) {
        console.log('WS Open');
        console.log('WS eventPhase: ' + event.eventPhase);
        console.log('WS readyState: ' + This._ws.readyState);
        This.on_open();
      };
      this._ws.onclose = function(event) {
        console.log('WS Close');
        This.on_close();
      };
      this._ws.onerror = function(event) {
        /* console.log('WS ERROR: readyState:' + this._ws.readyState); */
        This.on_error();
      };
      this._ws.onmessage = function(event) {
        console.log('WS Rx:' + event.data);
        This.on_message(event.data);
      };
    }

    on_message(data) {
      var blob_list = JSON.parse(data)
      this.onmessage(blob_list)
    }

    _retry_start(count) {
      if (this._retry_timer) {
        return;
      }
      this._retry_countdown = this._retry_countdown_init + 1;
      this._retry_wait();
      this._retry_countdown_init *= 2;
      this._retry_countdown_init = Math.min(this._retry_countdown_init, this._retry_max_delay);
    }

    _retry_stop() {
      this._retry_countdown = null;
      this._retry_countdown_init = this._retry_min_delay;
    }

    retry_now() {
      this._retry_countdown == 0;
      this.open();
    }

    _retry_wait() {
      this._retry_timer = null;
      if (this._retry_countdown <= 0) {
        return;
      }
      this._retry_countdown --;
      if (this._retry_countdown <= 0) {
        this.retry_now();
      } else {
        this.retry_countdown(this._retry_countdown);
        var This = this;
        this._retry_timer = setTimeout(function() {
          This._retry_wait();
        }, 1000);
      }
    }
}
