import logging

from mqtt_panel.web.widget.widget import Widget

class Dropdown(Widget):
    widget_type = 'dropdown'
    def __init__(self, *args, **kwargs):
        super(Dropdown, self).__init__(*args, **kwargs)

        self._value = ''
        self._text_map = {}
        for blob in self._c['values']:
            self._text_map[blob['payload']] = blob['text']

    def open(self):
        topic = self._c.get('subscribe', None)
        if not topic:
            topic = self._c.get('publish', None)
        if topic:
            self._mqtt.subscribe(topic, self._on_mqtt)
        else:
            logging.warning('No topic configured for "%s"', self.name)

    @property
    def _text(self):
        try:
            return self._text_map[self._value]
        except KeyError:
            return ''

    def _on_mqtt(self, payload, timestamp):
        logging.debug("Dropdown [%s] on_mqtt: %s", self.id, payload)
        if payload == self._value:
            return
        self._value = payload
        self._updated_now()
        self._update_clients()

    def on_widget(self, blob):
        logging.debug("Dropdown [%s] on_widget: %s", self.id, blob)

        value = blob['value']
        self._mqtt.publish(self._c['publish'], value,
                           retain=self._c['retain'], qos=self._c['qos'])
        return True

    def _blob(self):
        return {
            'value': self._value,
        }

    def _html(self, fh):
        self._write_render(fh, '''\
        <div class="value">
          <button type="button" data-bs-toggle="dropdown"></button>
          <ul>
        ''', indent=4)
        for blob in self._c['values']:
            href = f'javascript:on_widget_dropdown(\'{self.id}\', \'{blob["payload"]}\');'
            fh.write(f'        <li><a href="{href}">{blob["text"]}</a></li>\n')
        self._write_render(fh, '''\
          </ul>
        </div>
        ''', indent=4)


Widget.register(Dropdown)
