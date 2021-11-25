import hashlib
import json

from datetime import tzinfo, timedelta, datetime


class TZ(tzinfo):
    def __init__(self, minutes):
        super(TZ, self).__init__()
        self._minutes = minutes

    def utcoffset(self, dt):
        return timedelta(minutes=self._minutes)

    def dst(self, dt):
        return timedelta(0)


def now(tz_minutes):
    return datetime.now(tz=TZ(tz_minutes))


def now_ZA():
    return now(120)


def write_javascript(klass, fh, indent=0, context=None):
    import os
    import inspect
    import shutil
    script = os.path.splitext(inspect.getfile(klass))[0]
    if context:
        script += '.%s' % context
    script += '.js'
    try:
        with open(script, 'rt') as in_fh:
            fh.write('%s<script>\n' % (' ' * indent,))
            name = '%s: %s' % (klass.__name__, context) if context else klass.__name__
            fh.write('%s/* %s */\n' % (' ' * indent, name))
            for line in in_fh:
                if indent:
                    fh.write(' ' * indent)
                fh.write(line)
            fh.write('%s</script>\n' % (' ' * indent,))
    except FileNotFoundError:
        pass

def write_html(klass, fh, indent=0, context=None):
    import os
    import inspect
    import shutil
    script = os.path.splitext(inspect.getfile(klass))[0]
    if context:
        script += '.%s' % context
    script += '.html'
    try:
        with open(script, 'rt') as in_fh:
            name = '%s: %s' % (klass.__name__, context) if context else klass.__name__
            fh.write('%s<!-- %s -->\n' % (' ' * indent, name))
            for line in in_fh:
                if indent:
                    fh.write(' ' * indent)
                fh.write(line)
    except FileNotFoundError:
        pass

def blob_hash(blob):
    md5 = hashlib.md5()
    md5.update(json.dumps(blob, sort_keys=True).encode())
    return md5.hexdigest()
