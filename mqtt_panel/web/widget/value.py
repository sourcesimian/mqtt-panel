import logging

from mqtt_panel.web.widget.widget import Widget

class Value(Widget):
    widget_type = 'value'
    def __init__(self, *args, **kwargs):
        super(Value, self).__init__(*args, **kwargs)

    def open(self):
        self._mqtt.subscribe(self._c['subscribe'], self._on_mqtt)

    def _on_mqtt(self, payload, timestamp):

        try:
            txf = self._c.get('transform', None)
            if txf:
                txf = eval(txf)
                value = txf(payload)
            else:
                value = payload

            fmt = self._c.get('format', None)
            if fmt:
                value = fmt % value

        except Exception as ex:
            logging.warning('Ignored payload "%s" because "%s"', payload, ex)
            value = None

        self.set_value(value)

    def _blob(self):
        return {
            'value': self.value
        }

    def _html(self, fh):
        color = self._c.get('color', None)
        if color:
            color = ' style="color:%s"' % color

        icon = self._c.get('icon', '')

        self._write_render(fh, '''\
            <span class="material-icons"{color}>{icon}</span>
            <span class="value"{color}>{self.value}</span>
        ''', locals(), indent=4)


Widget.register(Value)