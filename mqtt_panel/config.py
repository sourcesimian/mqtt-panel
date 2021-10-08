import hashlib
import json
import logging
import os.path
import random

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


class Config(object):
    def __init__(self, config_file):
        logging.debug('Config file: %s', config_file)
        try:
            with open(config_file, 'rt') as fh:
                self._d = yaml.load(fh, Loader=yaml.Loader)
        except yaml.parser.ParserError as ex:
            logging.error('Loading %s: %s', config_file, ex)
            exit(1)

        logging.debug('Config: %s', self._d)
        # logging.debug('Config: %s', json.dumps(self._d, sort_keys=True))
        self._hash = hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()

        self._d['mqtt']['client-id'] += '-%s' % self._hash[8:]

    @property
    def cache(self):
        return self._d['cache']

    @property
    def http(self):
        return self._d['http']

    @property
    def html(self):
        return self._d.get('html', None) or {}

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


