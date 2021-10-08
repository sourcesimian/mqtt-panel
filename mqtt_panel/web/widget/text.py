from mqtt_panel.web.widget.widget import Widget

class Text(Widget):
    widget_type = 'text'
    def __init__(self, *args, **kwargs):
        super(Text, self).__init__(*args, **kwargs)
        self._text = ''

    def open(self):
        self._mqtt.subscribe(self._c['subscribe'], self._on_mqtt)

    def _on_mqtt(self, payload, timestamp):
        if payload == self._text:
            return
        self._text = payload
        self._updated_now()
        self._update_clients()

    def _blob(self):
        return {
            'text': self._text,
        }

    def _html(self, fh):
        color = self._c.get('color', None)

        if color:
            color = ' style="color:%s"' % color

        self._write_render(fh, '''\
            <div class="text"{color}></div>
        ''', locals(), indent=4)


Widget.register(Text)
