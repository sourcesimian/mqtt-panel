import logging
from mqtt_panel.web.widget.widget import Widget, WidgetCtx, WidgetBlob


class Text(Widget):
    widget_type = 'text'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    def open(self):
        self._mqtt.subscribe(self._c['subscribe'], self._on_mqtt)

    def _on_mqtt(self, payload, _timestamp):
        logging.info("{%s} Rx MQTT: %s", self.id, payload)
        self.set_value(payload)

    def _blob(self):
        return WidgetBlob({
            'value': self.value or '',
        })

    def _html(self, fh):
        blob = self._blob()
        ctx = WidgetCtx('color')
        ctx.color = self._c.get('color', None)

        if ctx.color:
            ctx.color = f' style="color:{ctx.color}"'

        self._write_render(fh, '''\
            <div class="text"{ctx.color}>{blob.value}</div>
        ''', {'ctx': ctx, 'blob': blob}, indent=4)
