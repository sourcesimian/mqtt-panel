import json
import logging

from mqtt_panel.web.widget.widget import Widget, WidgetBlob


class Gauge(Widget):
    widget_type = 'gauge'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._max = None
        self._min = None
        for value_range in self._iter_ranges():
            if self._min is None:
                self._min = value_range.start
            if self._max is None:
                self._max = value_range.end
            self._min = min(self._min, value_range.start)
            self._max = max(self._max, value_range.end)

    def open(self):
        self._mqtt.subscribe(self._c['subscribe'], self._on_mqtt)

    def _on_mqtt(self, payload, _timestamp):
        logging.info("{%s} Rx MQTT: %s", self.id, payload)
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

    def _current(self):
        value = self._value
        percent = 0
        if value is not None:
            percent = int((value - self._min) / (self._max - self._min) * 100)
        if value is not None:
            for value_range in self._iter_ranges():
                if value_range.start <= value <= value_range.end:
                    value_range['percent'] = percent
                    value_range['value'] = value
                    return value_range
        else:
            value = ''
        return WidgetBlob({
            'percent': percent,
            'value': value,
            'text': self._c.get('text', ''),
            'color': self._c.get('color', '#ccc'),
            'icon': self._c.get('icon', ''),
        })

    @property
    def _ranges(self):
        ranges = []
        for value_range in self._iter_ranges():
            ranges.append(value_range)
        ret = {'ranges': ranges}
        ret['min'] = self._min
        ret['max'] = self._max
        ret['text'] = self._c.get('text', '')
        ret['icon'] = self._c.get('icon', '')
        ret['color'] = self._c.get('color', '#ccc')

        return json.dumps(ret)

    def _blob(self):
        return WidgetBlob({
            'value': self._value,
        })

    def _data(self):
        return {
            'ranges': self._ranges,
            'value': self._value,
            'min': self._min,
            'max': self._max,
        }

    def _html(self, fh):
        current = self._current()

        data = ' '.join([f"data-{k}='{v}'" for k, v in self._data().items()])

        self._write_render(fh, '''\
            <span class="material-icons">{current.icon}</span>
            <span class="text">{current.text}</span><br>
            <div class="value" {data}>{current.value}}</div>
            <div class="meter"><span style="height:{current.percent}%;background-color={current.color}"></span></div>
        ''', {'data': data, 'current': current}, indent=4)

    def _iter_ranges(self):
        for blob in self._c['ranges']:
            start, end = blob.get('range', [None, None])
            value_range = WidgetBlob({
                'start': start,
                'end': end,
                'text': blob.get('text', self._c.get('text', '')),
                'icon': blob.get('icon', self._c.get('icon', '')),
                'color': blob.get('color', self._c.get('color', '#ccc')),
            })
            yield value_range
