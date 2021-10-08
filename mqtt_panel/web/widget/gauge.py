import collections
import logging

from mqtt_panel.web.widget.widget import Widget

class Gauge(Widget):
    widget_type = 'gauge'
    def __init__(self, *args, **kwargs):
        super(Gauge, self).__init__(*args, **kwargs)

    def open(self):
        self._mqtt.subscribe(self._c['subscribe'], self._on_mqtt)

    def _on_mqtt(self, payload, timestamp):
        logging.debug("{%s} Rx MQTT: %s", self.id, payload)
        # TODO: Validate
        try:
            value = float(payload)
        except ValueError:
            logging.warning('Ignoring payload: %s', payload)
            value = None

        if value is not None:
            if value > self.max:
                value = self.max
            if value < self.min:
                value = self.min

        self.set_value(value)

    def _blob(self):
        value = self.value
        text = self._c.get('text', '')
        icon = self._c.get('icon', '')
        color = self._c.get('color', None)
        width = '0%'

        if value is not None:
            for range in self._iter_ranges():
                if (range.start is not None and range.end is not None) \
                        and range.start <= value < range.end or \
                (range.start is not None and range.end is None) \
                        and range.start <= value or \
                (range.start is None and range.end is not None) \
                    and value < range.end:
                    if range.text:
                        text = range.text
                    if range.icon:
                        icon = range.icon
                    if range.color:
                        color = range.color
                    break
            width = '%d%%' % ((value - self.min) / (self.max - self.min) * 100)
        
        return {
            'value': value,
            'width': width,
            'text': text,
            'color': color,
            'icon': icon,
        }

    @property
    def max(self):
        return self._c['max']

    @property
    def min(self):
        return self._c['min']

    def _html(self, fh):
        id = '%s-meter' % self.id
        blob = self._blob()
        text = blob['text']
        color = ''
        if blob['color']:
            color = 'background-color:%s;' % blob['color']
        
        icon = blob['icon']
        width = blob['width']

        self._write_render(fh, '''\
          <!-- <div class="value" data-min="{self.min}" data-min="{self.max}"> -->
            <span class="material-icons">{icon}</span>
            <span class="text">{text}</span><br>
            <div class="meter">
                <span style="width:{width};{color}"></span>
                <div class="value">{self.value}</div>
            </div>
          <!-- </div> -->
        ''', locals(), indent=4)

    def _iter_ranges(self):
        for blob in self._c['range']:
            range = Range(
                blob.get('start', None),
                blob.get('end', None),
                blob.get('text', None),
                blob.get('color', None),
                blob.get('icon', None),
            )
            yield range


Widget.register(Gauge)

Range = collections.namedtuple('Range', ['start', 'end', 'text', 'color', 'icon'])
