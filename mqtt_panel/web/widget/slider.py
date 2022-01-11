import logging

from mqtt_panel.web.widget.gauge import Gauge


class Slider(Gauge):
    widget_type = 'slider'

    def on_widget(self, blob):
        payload = blob['value']
        logging.info('{%s} Publish "%s" %s', self.id, self._c['publish'], payload)
        self._mqtt.publish(self._c['publish'], payload,
                           retain=self._c.get('retain', False), qos=self._c.get('qos', 1))
        return True

    def _data(self):
        data = super()._data()
        data['live'] = self._c.get('live', False)
        return data
