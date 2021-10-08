class App {
    constructor() {
      this.appHash = '{self.hash}';
      this.serverOnline = false;
      this.mqttOnline = false;
      this.currentWidgets = [];
      this.onfocus_timeout = null;

      var This = this;
      this.titlebar = new TitleBar();
      this.menubar = new MenuBar(function(id) {
          return This.on_menubar(id);
      });
      this.fullScreen = new FullScreen();
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

      this.overlay = new LinkOverlay(function() {
          This.wslink.open();
      });
      
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

      $('.app').on('widget', function(event, blob) {
          This.on_widget(blob);
      });

      $('.app').on('register-widgets', function(event, widgets) {
        This.currentWidgets = widgets;
        This.on_register_widgets();
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
      /*
      if (blob.appHash != appHash) {
        window.location.reload();
      }
      */
      if ('action' in blob) {
        if (blob.action == 'disconnect') {
          window.location.reload();
        }
      }
      this.serverOnline = true;
      this.mqttOnline = blob.mqttOnline;
      this.on_online_change();
    }

    on_menubar(id) {
        if (id.startsWith('panel-')) {
          $('.panel').trigger('hide');
          $('.' + id).trigger('show');
          this.menubar.active(id);
          localStorage.setItem('panel', id);
          this.titlebar.title($('.' + id).data('title'));
          return false;
        }
        else if (id == 'fullscreen') {
          $('.fullscreen').trigger('toggle');
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
      window.location.href = 'logout';
    }

    on_message(blob_list) {
      this.on_focus_reset();
      var i;
      for (i in blob_list) {
        var blob = blob_list[i];
        if (blob.id.startsWith('w-')) {
          $('#' + blob.id).trigger("update", blob);
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
        this.overlay.update(this.serverOnline, this.mqttOnline);
    }
    
    on_offline() {
      console.log('offline');
      this.serverOnline = false;
      this.on_online_change();
    }

    update_panel() {
      var id = localStorage.getItem('panel');
      if (!id) {
        id = 'panel-{self._panels._panels[0].name}';
      }
      this.on_menubar(id);
    }

    on_online() {
        console.log('online');
    }

    on_retry_countdown(countdown) {
      this.overlay.countdown(countdown);
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
                lastUpdate = 'unknown';
            } else {
                lastUpdate = self.since(now, mtime);
            }

            $(this).find('.last-update').html(lastUpdate);
        });
    }
  }
  app = new App();

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
