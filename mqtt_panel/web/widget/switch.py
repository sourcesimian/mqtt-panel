import logging
import collections

from mqtt_panel.util import pad_string
from mqtt_panel.web.widget.widget import Widget, WidgetCtx


class Switch(Widget):
    widget_type = 'switch'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default = Default

        self._value_map = {}
        for idx, blob in enumerate(self._c['values']):
            self._value_map[blob['payload']] = idx

    def open(self):
        topic = self._c.get('subscribe', None)
        if not topic:
            topic = self._c.get('publish', None)
        if topic:
            self._mqtt.subscribe(topic, self._on_mqtt)
        else:
            logging.warning('No topic configured for "%s"', self.name)

    def _on_mqtt(self, payload, _timestamp):
        logging.info("{%s} Rx MQTT: %s", self.id, payload)
        try:
            value = self._value_map[payload]
        except KeyError:
            logging.warning('Unexpected MQTT value: %s', payload)
            value = None
        self.set_value(value)

    def on_widget(self, blob):
        payload = self._c['values'][blob['value']]['payload']
        logging.info('{%s} Publish "%s" %s', self.id, self._c['publish'], payload)
        self._mqtt.publish(self._c['publish'], payload,
                           retain=self._c.get('retain', False), qos=self._c.get('qos', 1))

        return True

    def _blob(self):
        return {
            'value': self.value
        }

    def _iter_states(self):

        max_text_len = 0
        for blob in self._c['values']:
            text = blob.get('text', '')
            max_text_len = max(max_text_len, len(text))

        for idx, blob in enumerate(self._c['values']):
            payload = blob['payload']
            text = blob.get('text', payload)
            text_padded = pad_string(text, max_text_len, '&nbsp;')
            next_idx = idx + 1
            try:
                self._c['values'][next_idx]
            except IndexError:
                next_idx = 0
            state = State(
                idx,
                text_padded,
                blob.get('icon', self.default.icon(text, payload)),
                blob.get('color', self.default.color(text, payload)),
                blob.get('confirm', None),
                next_idx,
                'true' if blob.get('read-only', False) else 'false',
            )
            yield state

        none_state = State(
            'null',
            'unknown',
            'do_not_disturb',
            None,
            None,
            0,
            True,
        )
        yield none_state

    def _html(self, fh):
        self._write_render(fh, '''\
            <div class="value">
        ''', indent=4)
        for state in self._iter_states():
            ctx = WidgetCtx('confirm', 'color', 'show')
            ctx.confirm = ''
            ctx.color = ''
            ctx.show = ' d-none'

            if state.confirm:
                ctx.confirm = f' data-confirm="{state.confirm}"'

            if state.color:
                ctx.color = f' style="color:{state.color};"'

            if state.name == self.value:
                ctx.show = ''

            self._html_write(fh, ctx, state)

        self._write_render(fh, '''\
            </div>
        ''', indent=4)

    def _html_write(self, fh, ctx, state):
        self._write_render(fh, '''\
            <div class="value-item value-{state.name}{ctx.show}"{ctx.confirm} data-next="{state.next}">
                <span class="material-icons"{ctx.color}>{state.icon}</span>
                <span{ctx.color}>{state.text}</span>
            </div>
        ''', {'ctx': ctx, 'state': state}, indent=6)


class Default:
    _map = {
        ('on', 'true'): ('toggle_on', '#52D017'),
        ('off', 'false'): ('toggle_off', 'black'),
        None: ('help_center', None),
    }

    @classmethod
    def _lookup(cls, *keys):
        for key in keys:
            key = key.lower()
            for k, v in cls._map.items():
                if k and key in k:
                    return v
        return cls._map[None]

    @classmethod
    def icon(cls, *key):
        return cls._lookup(*key)[0]

    @classmethod
    def color(cls, *key):
        return cls._lookup(*key)[1]


State = collections.namedtuple('State', ['name', 'text', 'icon', 'color', 'confirm', 'next', 'ro'])
