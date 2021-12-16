import logging

from mqtt_panel.web.widget.widget import Widget

class Image(Widget):
    widget_type = 'image'
    def __init__(self, *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)

    def open(self):
        value = self._c.get('src', None)
        if value:
            self.set_value(value)
        subscribe = self._c.get('subscribe', None)
        if subscribe:
            self._mqtt.subscribe(subscribe, self._on_mqtt)

    def _on_mqtt(self, payload, timestamp):
        logging.debug("Image [%s] on_mqtt: %s", self.id, payload)

        if not payload.startswith(('http://', 'https://')):
            logging.warning('Ignoring image payload: %s', payload)
            return
        self.set_value(payload)

    def _blob(self):
        return {
            'url': self.value
        }

    def _html(self, fh):
        attribs = ''
        if self._height:
            attribs += f' height="{self._height}"'
        if self._width:
            attribs += f' width="{self._width}"'
        self._write_render(fh, '''\
          <div class="image">
            <img src="{self.value}"{attribs}>
          </div>
        ''', locals(), indent=4)

    @property
    def _height(self):
        if self._c.get('height', None):
            return self._c["height"]

    @property
    def _width(self):
        if self._c.get('width', None):
            return self._c["width"]


Widget.register(Image)
