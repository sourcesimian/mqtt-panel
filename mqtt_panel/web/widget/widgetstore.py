import logging

class WidgetStore(object):
    def __init__(self):
        self._widget_map = {}

    def add_widget(self, widget):
        self._widget_map[widget.id] = widget

    def get_widget(self, widget_id):
        return self._widget_map[widget_id]

    def __iter__(self):
        for widget in self._widget_map.values():
            yield widget