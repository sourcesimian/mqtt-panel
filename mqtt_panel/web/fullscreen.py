from mqtt_panel.web.component import Component

class FullScreen(Component):
    def __init__(self):
        super(FullScreen, self).__init__(4)

    def _body(self, fh):
        self._write_render(fh, '''\
          <div id="fullscreen" class="d-none"></div>
        ''')
