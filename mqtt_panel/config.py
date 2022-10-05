import hashlib
import logging
import random
import sys

import yaml

# Prevent YAML loader from interpreting 'on', 'off', 'yes', 'no' as bool
from yaml.resolver import Resolver

for ch in "OoYyNn":
    Resolver.yaml_implicit_resolvers[ch] = [x for x in
                                            Resolver.yaml_implicit_resolvers[ch]
                                            if x[0] != 'tag:yaml.org,2002:bool']


def default(item, key, value):
    if key not in item:
        item[key] = value


class Config:
    def __init__(self, config_file):
        logging.info('Config file: %s', config_file)
        try:
            with open(config_file, 'rt', encoding="utf8") as fh:
                self._d = yaml.load(fh, Loader=yaml.Loader)
        except yaml.parser.ParserError as ex:
            logging.error('ScreenOverlay %s: %s', config_file, ex)
            sys.exit(1)

        self._hash = hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()

        # self._d['mqtt']['client-id'] += f'-{self._hash[8:]}'

    @property
    def log_level(self):
        try:
            level = self._d['logging']['level'].upper()
            return {
                'DEBUG': logging.DEBUG,
                'INFO': logging.INFO,
                'WARNING': logging.WARNING,
                'WARN': logging.WARNING,
                'ERROR': logging.ERROR,
            }[level]
        except KeyError:
            return logging.DEBUG

    @property
    def cache(self):
        return self._d['cache']

    @property
    def http(self):
        return self._d['http']

    @property
    def auth(self):
        return self._d.get('auth', None) or {}

    @property
    def mqtt(self):
        return self._d['mqtt']

    @property
    def groups(self):
        for item in self._d['groups']:
            yield item

    @property
    def panels(self):
        for item in self._d['panels']:
            yield item
