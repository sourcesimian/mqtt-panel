import logging
import os.path
import ssl
import sys
from typing import Dict

import paho.mqtt.client
import gevent

from .util import validate_path


def generate_mtls_context(config: Dict[str, str]):
    """builds the SSLContext required for Mutual-TLS (mTLS)

    Args:
        config (Dict[str, str]): defines the mTLS configuration
            cafile (str): path to the CA file used to verify the server
            certfile (str): path to the certificate presented by this client
                            for authentication
            keyfile (str): path to the private-key presented by this client for
                           authentication
            keyfile_password (str): password used to decrypt the `keyfile`, or
                                    `None`
            protocols (List[str]): list of alpn protocols to use for the mTLS
                                   handshake

    Returns:
        SSLContext: the SSLContext object to use for the client connection
    """
    ssl_context = ssl.create_default_context()
    ssl_context.set_alpn_protocols(config.get("protocols", []))

    if config.get("cafile", False):
        validate_path(config.get("cafile"))
        ssl_context.load_verify_locations(cafile=config.get("cafile"))

    if config.get("certfile", False) and config.get("keyfile", False):
        validate_path(config.get("certfile"))
        validate_path(config.get("keyfile"))
        ssl_context.load_cert_chain(
            certfile=config.get("certfile"),
            keyfile=config.get("keyfile"),
            password=config.get("keyfile_password", None)
        )

    return ssl_context


class Mqtt:
    def __init__(self, **config):
        self._subscribe_map = {}
        self._c = config
        self._topic_prefix = self._c.get('topic-prefix', None) or ''
        self._watchers = []
        self._client = None
        self.connect_timestamp = None

    def watch_online(self, on_change):
        self._watchers.append(on_change)

    def _notify_watchers(self, online):
        for watcher in self._watchers:
            gevent.spawn(watcher, online)

    def open(self):
        logging.info("Open (%s)", self._topic_prefix)
        self._client = paho.mqtt.client.Client(client_id=self._c['client-id'])
        self._client.start = paho.mqtt.client.time_func()

        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message = self._on_message

        _mqtt_auth = self._c.get('auth')
        if _mqtt_auth is None or _mqtt_auth.get('type') == 'none':
            logging.info('no mqtt auth defined')
        elif _mqtt_auth.get('type') == 'basic':
            logging.info('setting up basic auth')
            username = self._c.get('username', None)
            password = self._c.get('password', None)
            self._client.username_pw_set(username, password)
        elif _mqtt_auth.get('type') == 'mtls':
            logging.info('setting up mtls mqtt auth')
            mtls_context = generate_mtls_context(_mqtt_auth)
            self._client.tls_set_context(mtls_context)
        else:
            logging.warning('failed to determine mqtt auth settings')

        connect = {
            'host': self._c.get('host', '127.0.0.1'),
            'port': self._c.get('port', 1833),
            'keepalive': self._c.get('keepalive', 60),
            'bind_address': self._c.get('bind_address', ''),
            'bind_port': self._c.get('bind_port', 0),
            'properties': self._c.get('properties', None),
        }
        logging.info('Connecting to %s:%s', connect['host'], connect['port'])
        self._client.connect(**connect)

    def _on_connect(self, _client, _userdata, _flags, _rc):
        logging.info("On Connect")
        self.connect_timestamp = paho.mqtt.client.time_func()

        self._notify_watchers(True)

        for topic in self._subscribe_map:
            result, mid = self._client.subscribe(topic)
            logging.info('Subscribe "%s" [%s] %s', topic, paho.mqtt.client.error_string(result), mid)

    def run(self):
        return gevent.spawn(self._run_loop)

    def _run_loop(self):
        while True:
            try:
                self.open()
                self._client.loop_forever()
            except Exception as ex:     # pylint: disable=W0703
                logging.error('Run loop exception %s: %s', ex.__class__.__name__, ex)
                gevent.sleep(10)

    def close(self):
        logging.info("Close")
        if self._client:
            client = self._client
            self._client = None
            client.disconnect()

    def _on_disconnect(self, _client, _userdata, _rc):
        logging.info("On Disconnect")
        self._notify_watchers(False)

        if self._client:
            self.close()
            self.open()

    def _on_message(self, _client, _userdata, message):
        if self._topic_prefix and not message.topic.startswith(self._topic_prefix):
            logging.warning('Dropped message: %s', message)
            return

        try:
            payload = message.payload.decode()
            retained = ' (retained)' if message.retain else ''
            logging.debug("Received %s: %s%s", message.topic, payload, retained)
            for listener in self._subscribe_map[message.topic]:
                try:
                    listener(payload, message.timestamp)
                except Exception:
                    logging.exception('Handling MQTT message')
                    sys.exit(1)
        except KeyError:
            logging.exception('_on_message')

    def _topic(self, *p):
        if not p[0]:
            return None
        return os.path.join(self._topic_prefix, *p)

    def subscribe(self, topic, on_payload):
        topic = self._topic(topic)
        if topic not in self._subscribe_map:
            self._subscribe_map[topic] = []
        self._subscribe_map[topic].append(on_payload)

    def publish(self, topic, payload, retain=False, qos=0):
        if not topic:
            logging.warning('Ignoring empty topic')
            return
        topic = self._topic(topic)
        logging.debug("Publish %s: %s", topic, payload)
        self._client.publish(topic, payload=payload, qos=qos, retain=retain)
