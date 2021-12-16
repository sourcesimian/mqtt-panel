import logging

from mqtt_panel.web.widget.widget import Widget

class Light(Widget):
    widget_type = 'light'
    def __init__(self, *args, **kwargs):
        super(Light, self).__init__(*args, **kwargs)

        # self._value = self._c['values'][0].get('payload')
        self._payload_map = {}
        for blob in self._c['values']:
            self._payload_map[blob['payload']] = blob

    def open(self):
        self._mqtt.subscribe(self._c['subscribe'], self._on_mqtt)

    def _on_mqtt(self, payload, timestamp):
        logging.debug("Light [%s] on_mqtt: %s", self.id, payload)
        try:
            value = self._payload_map[payload]['payload']
        except KeyError as ex:
            logging.warning('Unexpected MQTT value: %s', payload)
            value = None
        self.set_value(value)

    def _blob(self):
        return {
            'value': self.value
        }

    def _html(self, fh):
        self._write_render(fh, '''\
            <div class="value">
        ''', indent=4)

        for blob in self._c['values']:
            value = blob.get('payload') 
            display = ''
            if self.value != value:
                display = ' d-none'
            
            text = blob.get('text', 'text')
            icon = blob.get('icon', Default.icon(text))
            color = blob.get('color', Default.color(text))

            self._write_render(fh, '''\
                <div class="value-item value-{value}{display}">
                    <span class="material-icons" style="color:{color};">{icon}</span>
                    <span style="color:{color};">{text}</span>
                </div>
            ''', locals(), indent=4)

        display = ''
        if self.value is not None:
            display = ' d-none'
        
        self._write_render(fh, '''\
              <div class="value-item value-null{display}">
                <span class="material-icons">do_not_disturb</span>
                <span>unknown</span>
              </div>
            </div>
        ''', locals(), indent=4)

class Default(object):
    _map = {
        ('on', 'true'): ('emoji_objects', 'yellow'),
        ('off', 'false'): ('emoji_objects','black'),
        None: ('help_center', None) 
    }
    @classmethod
    def _lookup(cls, key):
        key = key.lower()
        for keys in cls._map.keys():
            if keys and key in keys:
                return cls._map[keys]
        return cls._map[None]
    @classmethod
    def icon(cls, key):
        return cls._lookup(key)[0]
    @classmethod
    def color(cls, key):
        return cls._lookup(key)[1]


Widget.register(Light)
