from mqtt_panel.web.component import Component

class Modal(Component):
    def __init__(self):
        super(Modal, self).__init__(4)

    def _body(self, fh):
        self._write_render(fh, '''\
            <div id="modal" class="d-none"></div>
        ''', indent=self._indent)
