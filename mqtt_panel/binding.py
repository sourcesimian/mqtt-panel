import logging

from mqtt_panel.web.group import Group
from mqtt_panel.web.panel import Panel
from mqtt_panel.web.widget.widgetstore import WidgetStore
from mqtt_panel.web.app import App
from mqtt_panel.web.service import Service


class Binding:
    def __init__(self, cache, mqtt, groups, panels):
        self._cache = cache
        self._mqtt = mqtt
        self._groups = {}
        self._app = App()
        widget_store = self._init_groups(groups)
        self._service = Service(widget_store)
        self._init_panels(panels)

        self._app.add_menu('fullscreen', 'Fullscreen', 'fullscreen')
        self._app.add_menu('logout', 'Logout', 'logout')

    def _init_groups(self, groups):
        widget_store = WidgetStore(self._mqtt, self._cache)

        for group_blob in groups:
            group = Group(group_blob)
            for widget_blob in group_blob['widgets']:
                try:
                    widget = widget_store.add_widget(widget_blob)
                    group.add_widget(widget)
                except KeyError as ex:
                    logging.error('Can\'t create widget: %s %s: %s', ex.__class__.__name__, ex, widget_blob)

            self._groups[group.name] = group

        return widget_store

    def _init_panels(self, panels):
        for panel_blob in panels:
            panel = Panel(panel_blob)
            self._mqtt.watch_online(self._service.set_mqtt_online)

            for group_name in panel_blob['groups']:
                panel.add_group(self._groups[group_name])

            self._app.add_panel(panel)
            self._app.add_menu('panel-' + panel.name, panel.title, panel.icon)

    def open(self):
        self._app.open()

    def login(self, out):
        self._app.login(out)

    def app(self, out):
        self._app.html(out)

    def websocket(self, session, ws, env):
        self._service.web_socket(session, ws, env, self._app.identity)
