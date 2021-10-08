import itertools
import logging

from mqtt_panel.web.group import Group
from mqtt_panel.web.panel import Panel
from mqtt_panel.web.widget.widgetstore import WidgetStore
from mqtt_panel.web.widget.widget import Widget
from mqtt_panel.web.app import App
from mqtt_panel.web.service import Service

class Binding(object):
    def __init__(self, cache, mqtt, groups, panels, html):
        self._cache = cache
        self._mqtt = mqtt
        self._groups = {}
        self._app = App()
        # self._panel_page = Page(**html)
        widget_store = self._init_groups(groups)
        self._service = Service(widget_store)
        self._init_panels(panels)

        self._app.add_menu('fullscreen', 'Fullscreen', 'fullscreen')
        self._app.add_menu('logout', 'Logout', 'logout')


    def _init_groups(self, groups):
        counter = itertools.count(1)
        widget_store = WidgetStore()

        for group_blob in groups:
            group = Group(group_blob)
            for widget_blob in group_blob['widgets']:
                try:
                    klass = Widget.klaas(widget_blob['type'])
                    widget = klass(next(counter), widget_blob, self._mqtt, self._cache) 
                    group.add_widget(widget)
                    widget_store.add_widget(widget)
                except KeyError:
                    logging.error('Can\'t create widget "%s"', widget_blob['type'])

            self._groups[group.name] = group

        return widget_store

    def _init_panels(self, panels):
        counter = itertools.count(1)
        for panel_blob in panels:
            panel = Panel(panel_blob)
            self._mqtt.watch_online(self._service.mqtt_online)

            for group_name in panel_blob['groups']:
                panel.add_group(self._groups[group_name])

            self._app.add_panel(panel)
            self._app.add_menu('panel-' + panel.name, panel.title, panel.icon)


    def open(self):
        for group in self._groups.values():
            group.open()

    def login(self, out):
        self._app.login(out)

    def app(self, out):
        self._app.html(out)

    def websocket(self, session, ws, env):
        self._service.web_socket(session, ws, env)
