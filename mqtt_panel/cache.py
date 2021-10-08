import json
import logging
import os
import time
import pathlib


class Cache(object):
    def __init__(self, **config):
        self._root = config.get('root', 'cache')
        self._max_cache = config.get('max-cache', 86400 * 30)  # Cache for 30 days
        if not os.path.isdir(self._root):
            os.makedirs(self._root, exist_ok=True)
        now = time.time()
        for fname in pathlib.Path(self._root).iterdir():
            if not fname.is_file():
                continue
            if fname.stat().st_mtime < (now - self._max_cache):
                logging.info('Removing stale cache file: %s', fname)
                fname.unlink()

    def get(self, key):
        fname = self._value_file(key)
        try:
            with fname.open(mode='rt') as fh:
                value = json.load(fh)
                timestamp = fname.stat().st_mtime
                return timestamp, value
        except json.JSONDecodeError:
            fname.unlink()
        except FileNotFoundError:
            pass
        return None, None

    def set(self, key, timestamp, value):
        fname = self._value_file(key)
        try:
            with fname.open(mode='wt') as fh:
                json.dump(value, fh)
                os.utime(fname, (timestamp, timestamp))
            return
        except IOError:
            pass
        logging.warning('Failed to write cache file: %s', fname)

    def _value_file(self, key):
        key = key.replace('/', '~')
        return pathlib.Path(os.path.join(self._root, key + '.json'))
