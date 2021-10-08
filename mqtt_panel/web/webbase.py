import hashlib
import json
import logging
import re

import textwrap


class WebBase(object):
    def __init__(self, blob):
        self._c = blob
        self.__hash = self._calc_hash(self._c)

    @property
    def name(self):
        try:
            return self._c.get('name').replace(' ', '-').lower()
        except (KeyError, AttributeError):
            return self.title.replace(' ', '-').lower()

    @property
    def title(self):
        return self._c['title']

    @property
    def hash(self):
        return self.__hash

    @classmethod
    def _calc_hash(cls, c):
        md5 = hashlib.md5()
        cfg = json.dumps(c, sort_keys=True)
        md5.update(cfg.encode())
        return md5.hexdigest()

    @classmethod
    def _write_dedent(cls, fh, _text, indent=0):
        prefix = ' ' * indent
        fh.write(textwrap.indent(textwrap.dedent(_text), prefix))

    def _write_render(self, fh, _text, ctx=None, indent=0):
        ctx = ctx or {}
        ctx.update(locals())
        def repl(matchobj):
            return str(eval(matchobj.group(0)[1:-1], ctx))
        self._write_dedent(fh, re.sub('{[0-9A-Za-z.-_\[\]\(\)\"\' ]+}', repl, _text), indent=indent)
