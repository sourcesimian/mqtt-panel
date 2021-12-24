from collections import namedtuple
import importlib.metadata

from mqtt_panel.web.component import Component
from mqtt_panel.web.widget.widget import WidgetCtx


Action = namedtuple("Action", "id name icon")


class MenuBar(Component):
    def __init__(self):
        super().__init__(4)
        self._actions = []

    def add_action(self, menu_id, name, icon):
        self._actions.append(Action(menu_id, name, icon))

    def _body(self, fh):
        meta = dict(importlib.metadata.metadata('mqtt_panel'))
        ctx = WidgetCtx('version', 'url', 'author')
        ctx.version = meta['Version']
        ctx.url = meta['Home-page']
        ctx.author = meta['Author']

        self._write_render(fh, '''\
        <div class="menubar-overlay d-none">
        </div>
        <div class="menubar">
          <ul>
        ''', indent=self._indent)

        for action in self._actions:
            fh.write(f'    <li><a class="menubar-link" data-id="{action.id}"><span class="material-icons">{action.icon}</span> {action.name}</a></li>\n')

        self._write_render(fh, '''\
          </ul>
          <div class="menubar-version">
            <div>MQTT Panel</div>
            <div>author: <a href='{ctx.url}' target='_blank'>{ctx.author}</a></div>
            <div>version: {ctx.version}</div>
          </div>
        </div>
        ''', {'ctx': ctx}, indent=self._indent)
