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


def get_javascript(klass, fh, indent=0):
    import os
    import inspect
    import shutil
    script = os.path.splitext(inspect.getfile(klass))[0] + '.js'
    try:
        with open(script, 'rt') as in_fh:
            fh.write('%s<script>\n' % (' ' * indent,))
            fh.write('%s/* %s */\n' % (' ' * indent, klass.__name__))
            for line in in_fh:
                fh.write(line)
            fh.write('%s</script>\n' % (' ' * indent,))
    except FileNotFoundError:
        pass

