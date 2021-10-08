from mqtt_panel.web.component import Component

class LinkOverlay(Component):
    def __init__(self):
        super(LinkOverlay, self).__init__(4)

    def _body(self, fh):
        self._write_render(fh, '''\
            <div id="link-overlay" class="d-none">
                <div id="link-overlay-alert">Alert</div>
            </div>
            ''', indent=self._indent)
