class App {
    constructor() {
      this.serverOnline = false;
      this.mqttOnline = false;
      this.currentWidgets = [];
      this.onfocus_timeout = null;
      this._widget_id_prefix = 'w-';

      var This = this;
      this.titlebar = new TitleBar();
      this.menubar = new MenuBar(function(id) {
          return This.on_menubar(id);
      });
      this.fullScreen = new FullScreen();
      this.screenOverlay = new ScreenOverlay();
      this.modal = new Modal();
      this.wslink = new WSLink(
          function(msg) {
              This.on_message(msg);
          },
          function() {
              This.on_online();
          },
          function() {
              This.on_offline();
          },
          function(countdown) {
              This.on_retry_countdown(countdown);
          },
          'ws');

      this.mtimes = setInterval(function() {
          This.last_updates();
      }, 15000);

      $(window).blur(function(){
          This.on_blur();
      });

      $(window).focus(function(){
          This.on_focus();
      });

      $(document).ready(function() {
          This.wslink.open();
      });

      $('#app').on('widget', function(event, blob) {
          This.on_widget(blob);
      });

      $('#app').on('register-widgets', function(event, widgets) {
        This.currentWidgets = widgets;
        This.on_register_widgets();
      });

      $("#app").on("swipeleft", function(event){
        This.on_swipeleft(event);
      });
      $("#app").on("swiperight", function(event){
        This.on_swiperight(event);
      });
    }

    on_blur() {
      return;
    }

    on_focus() {
      this.on_focus_reset();
      var This = this;
      this.onfocus_timeout = setTimeout(function(){
        This.wslink.open();
      }, 5000);
      this.on_register_widgets();
      return;
    }

    on_focus_reset() {
      if (this.onfocus_timeout) {
        clearTimeout(this.onfocus_timeout);
        this.onfocus_timeout = null;
      }
    }

    update_app(blob) {
      if($('#app').data('identity') != blob.appIdentity) {
        $('#screen-overlay').trigger('spinner');
        window.location.reload();
      }
      if ('action' in blob) {
        if (blob.action == 'disconnect') {
          window.location.reload();
        }
      }
      this.serverOnline = true;
      this.mqttOnline = blob.mqttOnline;
      this.on_online_change();
    }

    show_panel(id) {
      $('.panel[data-id="' + id + '"]').trigger('show');

      this.menubar.active(id);
      localStorage.setItem('panel', id);
      this.titlebar.title($('.panel[data-id="' + id + '"]').data('title'));
    }

    on_menubar(id) {
        if (id.startsWith('panel-')) {
          this.show_panel(id);
          return false;
        }
        else if (id == 'fullscreen') {
          $('#fullscreen').trigger('toggle');
        }
        else if (id == 'logout') {
          this.logout();
          return true;
        }
        else {
          console.log("Menu Bar: " + id)
          return true;
        }              
    }

    logout() {
      fetch(
        './api/logout',
        {
          method: 'POST',
          credentials: 'same-origin',
        }
      )
      .then(response => response.json())
      .then(json => {
        document.cookie = json['session'];
        location.reload();
      })
      .catch( error => console.error('logout error:', error) );
    }

    on_message(blob_list) {
      this.on_focus_reset();
      var i;
      for (i in blob_list) {
        var blob = blob_list[i];
        if (blob.id.startsWith(this._widget_id_prefix)) {
          $('.widget[data-id="' + blob.id + '"]').trigger("update", blob);
        }
        else if (blob.id == 'app') {
          this.update_app(blob);
        }
        else {
          console.log('Unhandled Rx blob: '+ JSON.stringify(blob))
        }
      }
      this.last_updates();
    }

    on_widget(blob) {
      this.wslink.send([blob]);
    }

    confirm(prompt) {
      return confirm(prompt);
    }

    on_online_change() {
        if (this.serverOnline && this.mqttOnline) {
            $('.widget').trigger('enable');
            this.update_panel();
        } else{
            $('.widget').trigger('disable');
        }
        this.link_retry_update(this.serverOnline, this.mqttOnline);
    }
    
    on_offline() {
      console.log('offline');
      this.serverOnline = false;
      this.on_online_change();
    }

    link_retry_update(serverOnline, mqttOnline) {
      if (serverOnline && mqttOnline) {
        this.screenOverlay.hide();
      } else {
        this.screenOverlay.alert('Offline');
        this.screenOverlay.spinner();
      }
      if (!mqttOnline) {
        this.screenOverlay.alert('MQTT server offline');
        this.screenOverlay.spinner();
      }
    }

    update_panel() {
      let panelIds = this.panel_ids();
      let panelId = localStorage.getItem('panel');

      let index = panelIds.indexOf(panelId);
      if (index == -1) {
        panelId = panelIds[0];
      }

      this.on_menubar(panelId);
    }

    on_online() {
        console.log('online');
    }

    on_retry_countdown(countdown) {
      var span = $('<span> Link down</span>');
      span.prepend($('<span class="material-icons">cloud_off</span>'));
      if (countdown > 1) {
          span.append(navigator.onLine ? '' : '(you are offline)');
          span.append(' ... retry in ' + countdown + 's (tap to retry now)');
      } else {
          span.append(' ... retrying now');
      }
      this.screenOverlay.alert(span, function() {
        This.wslink.open();
      });
    }

    on_register_widgets() {
      this.wslink.send([{
        id: 'register',
        widgets: this.currentWidgets,
      }])
    }

    since(current, previous) {
      var msPerMinute = 60;
      var msPerHour = msPerMinute * 60;
      var msPerDay = msPerHour * 24;
      var msPerMonth = msPerDay * 30;
      var msPerYear = msPerDay * 365;

      var elapsed = current - previous;
      /*
      if (elapsed < msPerMinute) {
          return Math.round(elapsed) + ' seconds ago';
      }
      else
      */
      if (elapsed < msPerHour) {
          return Math.round(elapsed/msPerMinute) + ' minutes ago';
      }
      else if (elapsed < msPerDay ) {
          return Math.round(elapsed/msPerHour) + ' hours ago';
      }
      else if (elapsed < msPerMonth) {
          return Math.round(elapsed/msPerDay) + ' days ago';
      }
      else if (elapsed < msPerYear) {
          return Math.round(elapsed/msPerMonth) + ' months ago';
      }
      else {
          return Math.round(elapsed/msPerYear) + ' years ago';
      }
    }

    last_updates() {
        var now = Date.now()/1000;
        var self = this;
        $('.widget').map( function(elem) {
            var mtime = $(this).data('mtime');
            var lastUpdate;
            if (! mtime){
                lastUpdate = '-';
            } else {
                lastUpdate = self.since(now, mtime);
            }

            $(this).find('.last-update').html(lastUpdate);
        });
    }

    panel_ids() {
      return $('.panel').map(function() {
        return $(this).data('id');
      }).get();
    }

    move_panel(fn) {
      let panelIds = this.panel_ids()
      let currentId = $('.panel-active').data('id');
      let index = panelIds.indexOf(currentId);
      if (index == -1) {
          return;
      }
      let newId = panelIds[fn(index)];
      if (newId === undefined) {
          return;
      }
      this.show_panel(newId);
    }

    on_swipeleft(event) {
      this.move_panel(function(idx) {
        return idx + 1;
      });
    }

    on_swiperight(event) {
      this.move_panel(function(idx) {
        return idx - 1;
      });
    }
  }

  /* Bootstrap styling */

  $(document).ready(function() {
    // Flex
    //$(".box").addClass("container")

    // Link Overlay
    //$("#link-overlay").addClass("fixed-top");
    //$("#link-overlay-alert").addClass("fixed-top alert bg-warning text-center d-none");

    // Title Bar
    //$(".titlebar").addClass("fixed-top");

    // MenuBar
    //$("div.menubar ul").addClass("nav flex-column");
    //$("div.menubar ul li").addClass("nav-item");
    //$("div.menubar ul li a").addClass("nav-link list-group-item list-group-item-action");

    // Group
    //$("div.group div").addClass("card-group border-dark")

    // Widget
    //$("div.widget").addClass("card");
    //$("div.widget-body").addClass("card-body");
    //$("div.widget .last-update").addClass("text-muted");

    // Switch
    //$("div.widget-switch input").addClass("form-check-input");
    //$("div.widget-switch div.value").addClass("form-check form-switch");

    // Select
    $("div.widget-select select").addClass("custom-select");

    // Dropdown
    $("div.widget-dropdown div.value").addClass("dropdown");
    $("div.widget-dropdown button").addClass("btn btn-secondary btn-lg dropdown-toggle");
    $("div.widget-dropdown ul").addClass("dropdown-menu");
    $("div.widget-dropdown li a").addClass("dropdown-item");
});

let app = new App();
