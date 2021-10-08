import logging
import collections

from mqtt_panel.web.widget.widget import Widget

class Switch(Widget):
    widget_type = 'switch'
    def __init__(self, *args, **kwargs):
        super(Switch, self).__init__(*args, **kwargs)

        self._value_map = {}
        for key in self._iter_state_keys():
            self._value_map[self._c[key]['payload']] = key

    def open(self):
        topic = self._c.get('subscribe', None)
        if not topic:
            topic = self._c.get('publish', None)
        if topic:
            self._mqtt.subscribe(topic, self._on_mqtt)
        else:
            logging.warning('No topic configured for "%s"', self.name)

    def _on_mqtt(self, payload, timestamp):
        logging.debug("{%s} Rx MQTT: %s", self.id, payload)
        try:
            value = self._value_map[payload]
        except KeyError as ex:
            logging.error('Bad MQTT value: %s', payload)
            value = None
        self.set_value(value)

    def on_widget(self, blob):
        logging.debug("{%s} Rx widget: %s", self.id, blob)

        payload = self._c[blob['value']]['payload']
        self._mqtt.publish(self._c['publish'], payload,
                           retain=self._c.get('retain', False), qos=self._c.get('qos', 1))

        return True

    def _blob(self):
        return {
            'value': self.value
        }

    def _iter_state_keys(self):
        for key in self._c:
            if isinstance(self._c[key], dict):
                if 'payload' in self._c[key]:
                    if key == 'null':
                        logging.warning('Ignoring Switch state "null"')
                        continue
                    yield key

    def _iter_states(self):
        default_icon = {
            'on': 'toggle_on',
            'off': 'toggle_off',
        }
        default_color = {
            'on': '#52D017',
            'off': "black",
        }

        keys = list(self._iter_state_keys())

        for i, key in enumerate(keys):
            payload = self._c[key]['payload']
            try:
                next_state = keys[i + 1]
            except IndexError:
                next_state = keys[0]
            state = State(
                key,
                self._c[key].get('text', payload),
                self._c[key].get('icon', default_icon.get(key, 'help_center')),
                self._c[key].get('color', default_color.get(key, None)),
                self._c[key].get('confirm', None),
                self._c[key].get('next', next_state),
            )
            yield state

        try:
            next_state = self._c.get('default', keys[0])
        except IndexError:
            next_state = 'null'
        none_state = State(
            'null',
            'unknown',
            'do_not_disturb',
            None,
            None,
            next_state,
        )
        yield none_state

    def _html(self, fh):
        self._write_render(fh, '''\
            <div class="value">
        ''', indent=4)
        for state in self._iter_states():

            confirm = ''
            color = ''
            show = ' d-none'

            if state.confirm:
                confirm = f' data-confirm="{state.confirm}"'

            if state.color:
                color = f' style="color:{state.color};"'

            if state.name == self.value:
                show = ''

            self._write_render(fh, '''\
              <div class="value-item value-{state.name}{show}"{confirm} data-next="{state.next}">
                <span class="material-icons"{color}>{state.icon}</span>
                <span{color}>{state.text}</span>
              </div>
            ''', locals(), indent=6)
        
        self._write_render(fh, '''\
            </div>
        ''', locals(), indent=4)


Widget.register(Switch)

State = collections.namedtuple('State', ['name', 'text', 'icon', 'color', 'confirm', 'next'])
