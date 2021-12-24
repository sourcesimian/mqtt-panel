from mqtt_panel.web.widget.widget import Widget


class Iframe(Widget):
    widget_type = 'iframe'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._src = self._c['attr'].get('src', '')

    def open(self):
        topic = self._c.get('subscribe', None)
        if topic:
            self._mqtt.subscribe(topic, self._on_mqtt)

    def _on_mqtt(self, payload, _timestamp):
        if payload == self._src:
            return
        self._src = payload
        self._updated_now()
        self._update_clients()

    def _blob(self):
        return {
            'src': self._src
        }

    def _html(self, fh):
        self._write_render(fh, '<iframe src=""')
        for key, value in self._c.get('attr', []).items():
            if key == 'src':
                continue
            if self._c['attr'].get(key, None):
                fh.write(f' {key}="{value}"')
            else:
                fh.write(f' {key}')
        fh.write(' frameborder="0"></iframe>\n')
