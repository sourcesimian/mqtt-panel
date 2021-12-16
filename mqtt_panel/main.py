import sys
import logging

from functools import partial

import gevent
import gevent.monkey
from geventwebsocket.handler import WebSocketHandler

gevent.monkey.patch_all()
gevent.get_hub().SYSTEM_ERROR = BaseException

import mqtt_panel.binding
import mqtt_panel.config
import mqtt_panel.mqtt
import mqtt_panel.server

from mqtt_panel.cache import Cache

FORMAT = '%(asctime)-15s %(levelname)s [%(module)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

def cli():
    config_file = 'config.yaml' if len(sys.argv) < 2 else sys.argv[1]
    config = mqtt_panel.config.Config(config_file)

    logging.getLogger().setLevel(level=config.log_level)

    cache = Cache(**config.cache)

    mqtt = mqtt_panel.mqtt.Mqtt(**config.mqtt)

    binding = mqtt_panel.binding.Binding(cache, mqtt, config.groups, config.panels)

    server = mqtt_panel.server.Server(binding, config.http, config.auth)

    binding.open()

    # mqtt.open()
    if not server.open():
        return 1
    mqtt_loop = mqtt.run()

    try:
        gevent.joinall((mqtt_loop,))
    except KeyboardInterrupt:
        server.close()
        mqtt.close()

