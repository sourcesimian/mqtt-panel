from itertools import count

from mqtt_panel.util import blob_hash
from mqtt_panel.web.component import Component


class Panel(Component):
    def __init__(self, blob):
        super().__init__(blob)
        self._groups = []
        self._web_sockets = {}
        self._client_counter = count()

    def add_group(self, group):
        self._groups.append(group)

    def open(self):
        for group in self._groups:
            group.open()
        self._identity = blob_hash([g.identity for g in self._groups])

    @property
    def icon(self):
        return self._c.get('icon', 'dashboard')

    def _body(self, fh):
        fh.write(f'<div class="panel box d-none" data-title="{self.title}" data-id="panel-{self.name}">')
        for group in self._groups:
            group.html(fh)
            fh.write('\n')
        fh.write('</div>\n')

    def widgets(self):
        widgets = set()
        for group in self._groups:
            widgets.update(group.widget_classes())
        return widgets
