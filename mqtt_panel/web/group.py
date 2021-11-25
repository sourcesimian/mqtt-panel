import logging

from itertools import count

from mqtt_panel.web.webbase import WebBase


class Group(WebBase):
    def __init__(self, blob):
        super(Group, self).__init__(blob)

        self._widget_map = {}
        self._widgets = []
        self._web_sockets = {}
        self._client_counter = count()
        self._mqtt_online = False

    def add_widget(self, widget):
        self._widget_map[widget.id] = widget
        self._widgets.append(widget)

    @property
    def identity(self):
        md5 = hashlib.md5()
        for widget in self._widgets:
            md5.update(widget.identity)
        return md5.hexdigest()

    def open(self):
        for widget in self._widgets:
            widget.open()

    def gen_blobs(self):
        for widget in self._widgets:
            yield widget.blob()

    def html(self, fh):
        fh.write(f'<div class="group"><!-- {self.name} -->\n')
        fh.write(f'<div class="title">{self.title}</div>\n')
        fh.write(f'<div class="box">\n')
        for widget in self._widgets:
            fh.write(f'<!-- widget: {self.name} : {widget.name} [{widget.id}] -->\n')
            widget.html(fh)
            fh.write('\n')
        fh.write(f'</div>\n')
        fh.write(f'</div><!-- {self.name} -->\n')

    def widget_classes(self):
        for widget in self._widgets:
            yield widget.__class__
