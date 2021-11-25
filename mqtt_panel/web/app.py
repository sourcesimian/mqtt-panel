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
from mqtt_panel.util import write_javascript, write_html


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
          <title>MQTT Panel</title>
          </head>
          <body>
          ''')

        TitleBar()._body(fh)

        write_html(self.__class__, fh, indent=0, context='login')
        write_javascript(self.__class__, fh, indent=0, context='login')
        self._write_render(fh, '''\
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
        write_html(self.__class__, fh, indent=0, context='head')

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
        write_javascript(self.__class__, fh)
