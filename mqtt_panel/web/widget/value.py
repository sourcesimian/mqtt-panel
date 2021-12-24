import logging

from mqtt_panel.web.widget.widget import Widget, WidgetCtx


class Value(Widget):
    widget_type = 'value'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    def open(self):
        self._mqtt.subscribe(self._c['subscribe'], self._on_mqtt)

    def _on_mqtt(self, payload, _timestamp):

        try:
            txf = self._c.get('transform', None)
            if txf:
                txf = eval(txf)         # pylint: disable=W0123
                value = txf(payload)
            else:
                value = payload

            fmt = self._c.get('format', None)
            if fmt:
                value = fmt % value

        except Exception as ex:         # pylint: disable=W0703
            logging.warning('Ignored payload "%s" because "%s"', payload, ex)
            value = None

        self.set_value(value)

    def _blob(self):
        return {
            'value': self.value
        }

    def _html(self, fh):
        ctx = WidgetCtx('color', 'icon')
        ctx.color = self._c.get('color', None)
        if ctx.color:
            ctx.color = f' style="color:{ctx.color}"'

        ctx.icon = self._c.get('icon', '')

        self._write_render(fh, '''\
            <span class="material-icons"{ctx.color}>{ctx.icon}</span>
            <span class="value"{ctx.color}>{self.value}</span>
        ''', {'self': self, 'ctx': ctx}, indent=4)
