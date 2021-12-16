from contextlib import contextmanager
import logging
import os.path

from shutil import copyfileobj

from mqtt_panel.web.fullscreen import FullScreen
from mqtt_panel.web.menubar import MenuBar
from mqtt_panel.web.titlebar import TitleBar
from mqtt_panel.web.screenoverlay import ScreenOverlay
from mqtt_panel.web.modal import Modal
from mqtt_panel.web.wslink import WSLink
from mqtt_panel.web.webbase import WebBase
from mqtt_panel.web.panels import Panels
from mqtt_panel.web.widget.widget import Widget
from mqtt_panel.util import blob_hash, write_javascript, write_html, write_style

class App(WebBase):
    def __init__(self):
        super(App, self).__init__({})
        
        self._titlebar = TitleBar()
        self._menubar = MenuBar()
        self._screen_overlay = ScreenOverlay()

        self._components = [
            Modal(),
            self._screen_overlay,
            self._titlebar,
            self._menubar,
            WSLink(),
            FullScreen(),
        ]

        self._panels = Panels()

    def open(self):
      self._panels.open()
      self._identity = blob_hash([self._panels.identity])

    def add_panel(self, panel):
        self._panels.add_panel(panel)

    def add_menu(self, id, title, icon):
        self._menubar.add_action(id, title, icon)

    def login(self, fh):
        with self._in_html(fh):
          with self._in_head(fh):
            self._screen_overlay.head(fh)
            write_style(self.__class__, fh, indent=0, context='login')
            self._write_render(fh, '''\
              <style>
                .titlebar-toggle-menubar {
                  display: none;
                }
              </style>
              ''')

          with self._in_body(fh):
            TitleBar()._body(fh)
            self._screen_overlay.body(fh)

            write_html(self.__class__, fh, indent=0, context='login')
            self._screen_overlay.script(fh)
            write_javascript(self.__class__, fh, indent=0, context='login')

    def html(self, fh):
        with self._in_html(fh):
          with self._in_head(fh):
            for component in self._components:
                component.head(fh)

          with self._in_body(fh):
            for component in self._components:
              component.body(fh)

            fh.write('<div id="app" data-identity="%s">\n' % self.identity)
            fh.write('<div style="height:var(--titlebar-height)"><!-- pad for titlebar --></div>\n\n')
            self._panels.body(fh)
            fh.write('</div>\n')

            self._write_script(fh)

    def _write_script(self, fh):
        for component in self._components:
            component.script(fh)

        self._panels.script(fh)
        Widget.script(fh)
        Widget.scripts(fh)

        # Late JS includes
        self._write_dedent(fh, '''\
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script>
        ''')

        write_javascript(self.__class__, fh)

    @contextmanager
    def _in_html(self, fh):
        self._write_render(fh, '''\
          <!doctype html>
          <html>
        ''')
        yield
        self._write_render(fh, '''\
          </html>
        ''')

    @contextmanager
    def _in_head(self, fh):
        self._write_render(fh, '''\
          <head>
        ''')
        write_html(self.__class__, fh, indent=0, context='head')
        yield
        self._write_render(fh, '''\
          </head>
          ''')

    @contextmanager
    def _in_body(self, fh):
        self._write_render(fh, '''\
          <body>
        ''')
        yield
        self._write_render(fh, '''\
          </body>
        ''')
