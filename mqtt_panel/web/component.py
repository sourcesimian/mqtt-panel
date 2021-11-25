from mqtt_panel.web.webbase import WebBase
from mqtt_panel.util import write_javascript


class Component(WebBase):
    def __init__(self, blob=None, indent=0):
        super(Component, self).__init__(blob or {})
        self._indent = indent

    def head(self, fh):
        if hasattr(self, '_head'):
            fh.write('%s<!-- %s -->\n' % (' ' * self._indent, self.__class__.__name__))
            self._head(fh)

    def body(self, fh):
        if hasattr(self, '_body'):
            fh.write('%s<!-- %s -->\n' % (' ' * self._indent, self.__class__.__name__))
            self._body(fh)

    def script(self, fh):
        write_javascript(self.__class__, fh)
