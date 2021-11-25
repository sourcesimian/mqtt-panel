import itertools
import logging

from mqtt_panel.web.widget.widget import Widget


class WidgetStore(object):
    def __init__(self, mqtt, cache):
        self._widget_map = {}
        self._identity_map = {}
        self._ref_map = {}
        self._counter = itertools.count(1)
        self._mqtt = mqtt
        self._cache = cache

    def add_widget(self, widget_blob):
        try:
            klass = Widget.klaas(widget_blob['type'])
        except KeyError:
            try:
                if len(widget_blob.keys()) == 1:
                    return self._ref_map[widget_blob['ref']]
            except KeyError:
                pass
            raise

        widget = klass(next(self._counter), widget_blob, self._mqtt, self._cache)

        if widget.identity in self._identity_map:
            return self._identity_map[widget.identity]

        if widget.ref:
            if widget.ref in self._ref_map:
                raise KeyError('Ignoring duplicate ref "%s"' % widget.ref)
            self._ref_map[widget.ref] = widget
        self._identity_map[widget.identity] = widget
        self._widget_map[widget.id] = widget
        return widget

    def get_widget(self, widget_id):
        return self._widget_map[widget_id]

    def __iter__(self):
        for widget in self._widget_map.values():
            yield widget
