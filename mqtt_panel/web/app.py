import logging
import os.path

from shutil import copyfileobj

from mqtt_panel.web.fullscreen import FullScreen
from mqtt_panel.web.menubar import MenuBar
from mqtt_panel.web.titlebar import TitleBar
from mqtt_panel.web.linkoverlay import LinkOverlay
from mqtt_panel.web.modal import Modal
from mqtt_panel.web.wslink import WSLink
from mqtt_panel.web.webbase import WebBase
from mqtt_panel.web.panels import Panels
from mqtt_panel.web.widget.widget import Widget
from mqtt_panel.util import get_javascript


class App(WebBase):
    def __init__(self, **config):
        super(App, self).__init__(config)
        
        self._titlebar = TitleBar()
        self._menubar = MenuBar()

        self._components = [
            LinkOverlay(),
            Modal(),
            self._titlebar,
            self._menubar,
            WSLink(),
            FullScreen(),
        ]

        self._panels = Panels()

    def add_panel(self, panel):
        self._panels.add_panel(panel)

    def add_menu(self, id, title, icon):
        self._menubar.add_action(id, title, icon)

    def login(self, fh):
        self._write_render(fh, '''\
          <!doctype html>
          <html>
          <head>
        ''')

        self._write_head_meta(fh)

        self._write_render(fh, '''\
          <style>
            .titlebar-toggle-menubar {
              display: none;
            }
          </style>
          <title>MQTT Panel - Login</title>
          </head>
          <body>
          ''')

        TitleBar()._body(fh)

        self._write_render(fh, '''\
          <div class="login">
            <div>
              <h1>Login</h1>
              <form action="./login" method="post">
                <input type="hidden" id="user" name="user" value="user"><br><br>
                <input type="submit" value="Login">
              </form>
            <div>
          <div>
          </body>
          </html>
        ''')

    def html(self, fh):
        self._write_render(fh, '''\
          <!doctype html>
          <html>
          <head>
        ''')
        self._write_head_meta(fh)

        # data:image/x-icon;base64,{FAVICON}" />
        self._write_render(fh, '''\
          <title>MQTT Panel</title>
        ''', globals())

        for component in self._components:
            component.head(fh)

        self._write_render(fh, '''\
          </head>
          <body>
        ''')
        self._write_body(fh)
        self._write_script(fh)
        self._write_render(fh, '''\
          </body>
          </html>
        ''')

    def _write_head_meta(self, fh):
        # link = 'https://10.0.0.5/h/panel.home/'
        # <!-- <link rel="canonical" href="{link}"> -->
        self._write_render(fh, '''\
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

          <link rel="manifest" href="manifest.json">
          <meta name="theme-color" content="#272b30">

          <meta name="application-name" content="MQTT Panel">
          <link rel="shortcut icon" type="image/x-icon" href="favicon.ico">
          <link rel="icon" type="image/png" sizes="192x192" href="icon-192x192.png">

          <!-- Apple -->
          <link rel="apple-touch-icon" type="image/png" sizes="192x192" href="ios-icon-192x192.png">
          <meta name="apple-mobile-web-app-capable" content="yes">
          <meta name="apple-mobile-web-app-title" content="MQTT Panel">
          <meta name="apple-mobile-web-app-status-bar-style" content="black">
          <meta name="apple-mobile-web-app-title" content="MQTT Panel">

          <!--
          <meta name="mobile-web-app-capable" content="yes">
          <meta name="msapplication-navbutton-color" content="#333333">
          <meta name="msapplication-starturl" content="/">
          -->

          <!-- jQuery Javascript -->
          <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>

          <!-- Icons -->
          <link href="https://fonts.googleapis.com/css2?family=Material+Icons" rel="stylesheet">

          <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">
          <link rel="stylesheet" href="theme.css">
          <link rel="stylesheet" href="style.css">
        ''', locals())

    def _write_body(self, fh):
        for component in self._components:
            component.body(fh)

        fh.write('<div class="app">\n')
        self._panels.body(fh)
        fh.write('</div>\n')

    def _write_script(self, fh):
        for component in self._components:
            component.script(fh)

        self._panels.script(fh)
        Widget.script(fh)
        Widget.scripts(fh)

        self._write_late_js_includes(fh)
        self._write_body_js(fh)

    def _write_late_js_includes(self, fh):
        self._write_dedent(fh, '''\
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script>
        ''')

    def _write_body_js(self, fh):
        get_javascript(self.__class__, fh)
