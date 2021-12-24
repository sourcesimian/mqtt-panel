import logging

from mqtt_panel.web.widget.widget import Widget, WidgetCtx


class Button(Widget):
    widget_type = 'button'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

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
        ctx = WidgetCtx('icon', 'color', 'text', 'confirm')
        ctx.icon = self._c.get('icon', 'touch_app')
        ctx.color = self._c.get('color', 'white')
        ctx.text = self._c.get('text', '')
        ctx.confirm = self._c.get('confirm', None)

        if ctx.color:
            ctx.color = f' style="color:{ctx.color}"'

        if ctx.confirm:
            ctx.confirm = f' data-confirm="{ctx.confirm}"'

        self._write_render(fh, '''\
            <div class="value"{ctx.confirm}>
              <span class="material-icons"{ctx.color}>{ctx.icon}</span>
              <span{ctx.color}>{ctx.text}</span>
            </div>
        ''', {'ctx': ctx}, indent=4)
