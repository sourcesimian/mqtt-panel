import logging

from mqtt_panel.web.widget.widget import Widget, WidgetBlob

class Gauge(Widget):
    widget_type = 'gauge'
    def __init__(self, *args, **kwargs):
        super(Gauge, self).__init__(*args, **kwargs)

        self._max = None
        self._min = None
        for range in self._iter_ranges():
            if self._min is None:
                self._min = range.start
            if self._max is None:
                self._max = range.end
            self._min = min(self._min, range.start)
            self._max = max(self._max, range.end)

    def open(self):
        self._mqtt.subscribe(self._c['subscribe'], self._on_mqtt)

    def _on_mqtt(self, payload, timestamp):
        logging.debug("{%s} Rx MQTT: %s", self.id, payload)
        # TODO: Validate
        try:
            if '.' in payload:
                value = float(payload)
            else:
                value = int(payload)
        except ValueError:
            logging.warning('Ignoring payload: %s', payload)
            value = None

        if value is not None:
            if value > self._max:
                value = self._max
            if value < self._min:
                value = self._min

        self.set_value(value)

    def _blob(self):
        value = self.value
        text = self._c.get('text', '')
        icon = self._c.get('icon', '')
        color = self._c.get('color', '#ccc')
        percent = 0

        if value is not None:
            for range in self._iter_ranges():
                if range.start <= value <= range.end:
                    if range.text:
                        text = range.text
                    if range.icon:
                        icon = range.icon
                    if range.color:
                        color = range.color
                    break
            percent =  int((value - self._min) / (self._max - self._min) * 100)
        
        return WidgetBlob({
            'value': value,
            'percent': percent,
            'text': text,
            'color': color,
            'icon': icon,
        })

    def _html(self, fh):
        blob = self._blob()

        self._write_render(fh, '''\
          <!-- <div class="value" data-min="{self._min}" data-min="{self._max}"> -->
            <span class="material-icons">{blob.icon}</span>
            <span class="text">{blob.text}</span><br>
            <div class="value">{blob.value}</div>
            <div class="meter"><span style="height:{blob.percent};background-color={blob.color}"></span></div>
          <!-- </div> -->
        ''', locals(), indent=4)

    def _iter_ranges(self):
        for blob in self._c['ranges']:
            start, end = blob.get('range', [None, None])
            range = WidgetBlob({
                'start': start,
                'end': end,
                'text': blob.get('text', None),
                'color': blob.get('color', None),
                'icon': blob.get('icon', None),
            })
            yield range


Widget.register(Gauge)
