from collections import namedtuple
import importlib.metadata

from mqtt_panel.web.component import Component

Action = namedtuple("Action", "id name icon")

class MenuBar(Component):
    def __init__(self):
        super(MenuBar, self).__init__(4)
        self._actions = []

    def add_action(self, id, name, icon):
        self._actions.append(Action(id, name, icon))

    def _body(self, fh):
        meta = dict(importlib.metadata.metadata('mqtt_panel'))
        version = meta['Version']
        url = meta['Home-page']
        author = meta['Author']

        self._write_render(fh, '''\
        <div class="menubar-overlay d-none">
        </div>
        <div class="menubar">
          <ul>
        ''', locals(), indent=self._indent)

        for action in self._actions:
            fh.write(f'    <li><a class="menubar-link" data-id="{action.id}"><span class="material-icons">{action.icon}</span> {action.name}</a></li>\n')

        self._write_render(fh, '''\
          </ul>
          <div class="menubar-version">
            <div>MQTT Panel</div>
            <div>author: <a href='{url}' target='_blank'>{author}</a></div>
            <div>version: {version}</div>
          </div>
        </div>
        ''', locals(), indent=self._indent)
