from mqtt_panel.web.webbase import WebBase
from mqtt_panel.util import write_javascript, write_style


class Component(WebBase):
    def __init__(self, blob=None, indent=0):
        super().__init__(blob or {})
        self._indent = indent

    def head(self, fh):
        write_style(self.__class__, fh)
        if hasattr(self, '_head'):
            indent = ' ' * self._indent
            fh.write(f'{indent}<!-- {self.__class__.__name__} -->\n')
            self._head(fh)

    def body(self, fh):
        if hasattr(self, '_body'):
            indent = ' ' * self._indent
            fh.write(f'{indent}<!-- {self.__class__.__name__} -->\n')
            self._body(fh)

    def script(self, fh):
        write_javascript(self.__class__, fh)
