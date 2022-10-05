import importlib.metadata
import logging
import sys

import gevent
import gevent.monkey
from geventwebsocket.handler import WebSocketHandler        # noqa: E402,F401 pylint: disable=W0611

gevent.monkey.patch_all()
gevent.get_hub().SYSTEM_ERROR = BaseException

import mqtt_panel.binding                                   # noqa: E402 pylint: disable=C0413,C0412
import mqtt_panel.config                                    # noqa: E402 pylint: disable=C0413,C0412
import mqtt_panel.mqtt                                      # noqa: E402 pylint: disable=C0413,C0412
import mqtt_panel.server                                    # noqa: E402 pylint: disable=C0413,C0412

from mqtt_panel.cache import Cache                          # noqa: E402 pylint: disable=C0413,C0412
from mqtt_panel.web.widget.widgets import register_widgets  # noqa: E402 pylint: disable=C0413,C0412


register_widgets()


FORMAT = '%(asctime)-15s %(levelname)s [%(module)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


def cli():
    meta = dict(importlib.metadata.metadata('mqtt_panel'))
    logging.info('Running mqtt-panel v%s', meta['Version'])

    config_file = 'config.yaml' if len(sys.argv) < 2 else sys.argv[1]
    config = mqtt_panel.config.Config(config_file)

    logging.getLogger().setLevel(level=config.log_level)

    cache = Cache(**config.cache)

    mqtt = mqtt_panel.mqtt.Mqtt(config.mqtt)

    binding = mqtt_panel.binding.Binding(cache, mqtt, config.groups, config.panels)

    server = mqtt_panel.server.Server(binding, config.http, config.auth)

    binding.open()

    # mqtt.open()
    if not server.open():
        return 1
    mqtt_loop = mqtt.run()

    try:
        gevent.joinall(mqtt_loop)
    except KeyboardInterrupt:
        server.close()
        mqtt.close()
    return 0
