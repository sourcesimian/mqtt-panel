import logging

from mqtt_panel.web.widget.widget import Widget

class Button(Widget):
    widget_type = 'button'
    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)

    def open(self):
        pass

    def on_widget(self, blob):
        logging.debug("{%s} Rx widget: %s", self.id, blob)

        payload = self._c['payload']
        self._mqtt.publish(self._c['publish'], payload,
                           retain=self._c.get('retain', False), qos=self._c.get('qos', 1))

        self._updated_now()
        self._update_clients()
        return True

    def _blob(self):
        return {
        }

    def _html(self, fh):
        icon = self._c.get('icon', 'touch_app')
        color = self._c.get('color', 'white')
        text = self._c.get('text', '')
        confirm = self._c.get('confirm', None)

        if color:
            color = ' style="color:%s"' % color

        if confirm:
            confirm = f' data-confirm="{confirm}"'
        
        self._write_render(fh, '''\
            <div class="value"{confirm}>
              <span class="material-icons"{color}>{icon}</span>
              <span{color}>{text}</span>
            </div>
        ''', locals(), indent=4)

Widget.register(Button)