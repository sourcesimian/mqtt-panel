from itertools import count
from mqtt_panel.util import blob_hash

from mqtt_panel.web.webbase import WebBase


class Group(WebBase):
    def __init__(self, blob):
        super().__init__(blob)

        self._open = False
        self._widget_map = {}
        self._widgets = []
        self._web_sockets = {}
        self._client_counter = count()

    def add_widget(self, widget):
        self._widget_map[widget.id] = widget
        self._widgets.append(widget)

    def open(self):
        if self._open:
            return
        for widget in self._widgets:
            widget.open()
        self._identity = blob_hash([w.identity for w in self._widgets])
        self._open = True

    def html(self, fh):
        fh.write(f'<div class="group"><!-- {self.name} -->\n')
        fh.write(f'<div class="title">{self.title}</div>\n')
        fh.write('<div class="box">\n')
        for widget in self._widgets:
            fh.write(f'<!-- widget: {self.name} : {widget.name} [{widget.id}] -->\n')
            widget.html(fh)
            fh.write('\n')
        fh.write('</div>\n')
        fh.write(f'</div><!-- {self.name} -->\n')

    def widget_classes(self):
        for widget in self._widgets:
            yield widget.__class__
