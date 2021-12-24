from mqtt_panel.web.component import Component


class ScreenOverlay(Component):
    def __init__(self):
        super().__init__(4)

    def _body(self, fh):
        self._write_render(fh, '''\
            <div id="screen-overlay" class="d-none">
                <div class="alert d-none">Alert</div>
                <div class="spinner d-none"></div>
            </div>
        ''', indent=self._indent)
