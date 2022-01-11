from contextlib import contextmanager

from mqtt_panel.web.fullscreen import FullScreen
from mqtt_panel.web.menubar import MenuBar
from mqtt_panel.web.titlebar import TitleBar
from mqtt_panel.web.screenoverlay import ScreenOverlay
from mqtt_panel.web.modal import Modal
from mqtt_panel.web.wslink import WSLink
from mqtt_panel.web.group import Group
from mqtt_panel.web.panel import Panel
from mqtt_panel.web.panels import Panels
from mqtt_panel.web.widget.widget import Widget
from mqtt_panel.util import write_javascript, write_html, write_style
from mqtt_panel.web.component import Component


class App(Component):
    def __init__(self):
        super().__init__({})

        self._identity = None
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
        self._identity = self._panels.identity

    def add_panel(self, panel):
        self._panels.add_panel(panel)

    def add_menu(self, menu_id, title, icon):
        self._menubar.add_action(menu_id, title, icon)

    def login(self, fh):
        with self._in_html(fh):
            with self._in_head(fh):
                self.style(fh)
                self._titlebar.head(fh)
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
                self._titlebar.body(fh)
                self._screen_overlay.body(fh)
                write_html(self.__class__, fh, indent=0, context='login')
                self._screen_overlay.script(fh)
                write_javascript(self.__class__, fh, indent=0, context='login')

    def html(self, fh):
        with self._in_html(fh):
            with self._in_head(fh):
                self.style(fh)
                for component in self._components:
                    component.head(fh)
                Panel.style(fh)
                Group.style(fh)
                Widget.style(fh)

            with self._in_body(fh):
                for component in self._components:
                    component.body(fh)

                fh.write('<!-- App -->\n')
                fh.write(f'<div id="app" data-identity="{self.identity}">\n')
                fh.write('<div style="height:var(--titlebar-height)"><!-- pad for titlebar --></div>\n\n')
                self._panels.body(fh)
                fh.write('</div>\n')

                for component in self._components:
                    component.script(fh)

                self._panels.script(fh)
                Widget.script(fh)

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
