import logging

from mqtt_panel.web.widget.widget import Widget

class Select(Widget):
    widget_type = 'select'
    def __init__(self, *args, **kwargs):
        super(Select, self).__init__(*args, **kwargs)

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
        logging.debug("Select [%s] on_mqtt: %s", self.id, payload)
        if payload == self._value:
            return
        self._value = payload
        self._updated_now()
        self._update_clients()

    def _update_mqtt(self):
        self._mqtt.publish(self._c['publish'], self._value,
                           retain=self._c.get('retain', False),
                           qos=self._c.get('qos', 0))

    def on_widget(self, blob):
        logging.debug("Select [%s] on_widget: %s", self.id, blob)
        if blob['value'] == self._value:
            return False
        self._value = blob['value']
        self._updated_now()
        self._update_mqtt()
        return True

    def _blob(self):
        return {
            'value': self._value,
        }

    def _html(self, fh):
        self._write_render(fh, '''\
          <div class="value">
            <select data-id="{self.id}">
            <option selected></option>
        ''', indent=4)
        for blob in self._c['values']:
            fh.write(f'      <option value="{blob["payload"]}">{blob["text"]}</option>\n')
        self._write_render(fh, '''\
            </select>
          </div>
        ''', indent=4)


Widget.register(Select)
