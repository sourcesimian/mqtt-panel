import logging
import time

from mqtt_panel.web.webbase import WebBase
from mqtt_panel.util import write_javascript


class Widget(WebBase):
    widget_type = 'widget'
    _id_prefix = 'w-'
    _widgets = {}

    def __init__(self, index, blob, mqtt, cache):
        super().__init__(blob)

        try:
            self.ref = blob['ref']
        except KeyError:
            self.ref = None

        self.__id = self._id_prefix + str(index)
        self._mqtt = mqtt
        self._cache = cache

        self._on_update_widget = None

        if self._c.get('cache', False) is True:
            self.__last_update, self._value = self._cache.get(self._cache_key('value'))
        else:
            self.__last_update, self._value = None, None

    def open(self):
        logging.warning('open() not implemented for "%s"', self.widget_type)

    def close(self):
        logging.warning('close() not implemented for "%s"', self.widget_type)

    @property
    def id(self):
        return self.__id

    def set_update_widget(self, update_widget):
        self._on_update_widget = update_widget

    def _updated_now(self):
        self.__last_update = time.time()

    def _update_clients(self):
        self._on_update_widget(self.blob())

    @property
    def _mtime(self):
        if self.__last_update is None:
            return None
        return self.__last_update

    def on_widget(self, blob):
        logging.warning('on_widget() not implemented for "%s": %s', self.widget_type, blob)

    def _cache_key(self, key):
        return f'widget/{self.identity}/{key}'

    def set_value(self, value):
        self._value = value
        self._updated_now()
        if self._c.get('cache', False) is True:
            self._cache.set(self._cache_key('value'), self.__last_update, self._value)
        self._update_clients()

    @property
    def value(self):
        return self._value

    def html(self, fh):
        self._write_render(fh, '''\
            <div class="widget widget-{self.widget_type} noselect" data-id="{self.id}" data-mtime="" data-value="{self.value}">
              <div class="body">
                <div class="title">{self.title}</div>
            ''', {'self': self})

        self._html(fh)

        self._write_render(fh, '''\
                <div class="last-update">-</div>
              </div>
            </div>
        ''')

    def _html(self, fh):
        logging.warning('html() not implemented for "%s"', self.widget_type)
        fh.write(f'<div>Not implemented: {self.widget_type}</div>\n')

    def blob(self):
        blob = self._blob()
        if blob is None:
            return None
        blob['id'] = self.id
        blob['mtime'] = self._mtime
        return blob

    def _blob(self):
        logging.warning('_blob() not implemented for "%s"', self.widget_type)
        return {}

    @classmethod
    def script(cls, fh):
        write_javascript(cls, fh)

    @classmethod
    def scripts(cls, fh):
        for widget_type in sorted(cls._widgets):
            write_javascript(cls._widgets[widget_type], fh)

    @classmethod
    def klaas(cls, class_type):
        return cls._widgets[class_type]

    @classmethod
    def register(cls, klaas):
        assert klaas.widget_type not in cls._widgets
        cls._widgets[klaas.widget_type] = klaas


class WidgetBlob(dict):
    def __init__(self, d):
        super().__init__()
        for k, v in d.items():
            self[k] = v

    def __getattr__(self, key):
        if key in self:
            return self[key]
        return super().__getitem__(key)


class WidgetCtx(dict):
    def __init__(self, *keys):
        super().__init__()
        for key in keys:
            self[key] = None

    def __setattr__(self, key, value):
        if key in self:
            self[key] = value
            return
        raise KeyError(key)

    def __getattr__(self, key):
        if key in self:
            return self[key]
        raise KeyError(key)
