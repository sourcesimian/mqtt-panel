import logging

from mqtt_panel.web.widget.widget import Widget, WidgetCtx


class Image(Widget):
    widget_type = 'image'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    def open(self):
        value = self._c.get('src', None)
        if value:
            self.set_value(value)
        subscribe = self._c.get('subscribe', None)
        if subscribe:
            self._mqtt.subscribe(subscribe, self._on_mqtt)

    def _on_mqtt(self, payload, _timestamp):
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
        ctx = WidgetCtx('attribs')
        ctx.attribs = ''
        if self._height:
            ctx.attribs += f' height="{self._height}"'
        if self._width:
            ctx.attribs += f' width="{self._width}"'
        self._write_render(fh, '''\
          <div class="image">
            <img src="{self.value}"{ctx.attribs}>
          </div>
        ''', {'self': self, 'ctx': ctx}, indent=4)

    @property
    def _height(self):
        if self._c.get('height', None):
            return self._c["height"]
        return None

    @property
    def _width(self):
        if self._c.get('width', None):
            return self._c["width"]
        return None
