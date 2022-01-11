import logging

from mqtt_panel.web.widget.widget import Widget, WidgetCtx


class Light(Widget):
    widget_type = 'light'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self._value = self._c['values'][0].get('payload')
        self._payload_map = {}
        for blob in self._c['values']:
            self._payload_map[blob['payload']] = blob

    def open(self):
        self._mqtt.subscribe(self._c['subscribe'], self._on_mqtt)

    def _on_mqtt(self, payload, _timestamp):
        logging.info("{%s} Rx MQTT: %s", self.id, payload)
        try:
            value = self._payload_map[payload]['payload']
        except KeyError:
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
            ctx = WidgetCtx('value', 'display', 'text', 'icon', 'color')
            ctx.value = blob.get('payload')
            ctx.display = ''
            if self.value != ctx.value:
                ctx.display = ' d-none'

            ctx.text = blob.get('text', 'text')
            ctx.icon = blob.get('icon', Default.icon(ctx.text))
            ctx.color = blob.get('color', Default.color(ctx.text))

            self._write_render(fh, '''\
                <div class="value-item value-{ctx.value}{ctx.display}">
                    <span class="material-icons" style="color:{ctx.color};">{ctx.icon}</span>
                    <span style="color:{ctx.color};">{ctx.text}</span>
                </div>
            ''', {'ctx': ctx}, indent=4)

        ctx.display = ''
        if self.value is not None:
            ctx.display = ' d-none'

        self._write_render(fh, '''\
                <div class="value-item value-null{ctx.display}">
                    <span class="material-icons">do_not_disturb</span>
                    <span>unknown</span>
                </div>
            </div>
        ''', {'ctx': ctx}, indent=4)


class Default:
    _map = {
        ('on', 'true'): ('emoji_objects', 'yellow'),
        ('off', 'false'): ('emoji_objects', 'black'),
        None: ('help_center', None),
    }

    @classmethod
    def _lookup(cls, key):
        key = key.lower()
        for k, v in cls._map.items():
            if k and key in k:
                return v
        return cls._map[None]

    @classmethod
    def icon(cls, key):
        return cls._lookup(key)[0]

    @classmethod
    def color(cls, key):
        return cls._lookup(key)[1]
