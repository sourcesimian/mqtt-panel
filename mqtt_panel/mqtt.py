import logging
import os.path
import re
import ssl
import sys

import paho.mqtt.client
import gevent


class Mqtt:
    def __init__(self, config):
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

        auth = self._c.get('auth', None)
        if auth:
            auth_type = auth.get('type', 'none')

            if auth_type == 'basic':
                logging.info('Using basic auth')
                username = auth.get('username', None)
                password = auth.get('password', None)
                self._client.username_pw_set(username, password)

            elif auth_type == 'mtls':
                logging.info('Using mTLS auth')

                mtls_context = ssl.create_default_context()
                mtls_context.set_alpn_protocols(auth.get("protocols", []))

                cafile = auth.get("cafile", None)
                if cafile:
                    mtls_context.load_verify_locations(cafile=cafile)

                certfile = auth.get("certfile", None)
                keyfile = auth.get("keyfile", None)
                keyfile_password = auth.get("keyfile_password", None)
                if certfile and keyfile:
                    mtls_context.load_cert_chain(
                        certfile=certfile,
                        keyfile=keyfile,
                        password=keyfile_password,
                    )

                self._client.tls_set_context(mtls_context)

            else:
                logging.warning('Ignoring unknown auth type: %s', auth_type)

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

    def _on_connect(self, _client, _userdata, flags, rc):
        if rc != 0:
            logging.error("Bad Connect: %s rc=%s", flags, rc)
            return

        logging.info("On Connect: %s", flags)
        self.connect_timestamp = paho.mqtt.client.time_func()

        self._notify_watchers(True)

        for matcher in self._subscribe_map:
            result, _mid = self._client.subscribe(matcher.topic)
            error = paho.mqtt.client.error_string(result)
            if error != 'No error.':
                logging.warning('Subscribe "%s" with %s', matcher.topic, error)
            else:
                logging.debug('Subscribe "%s"', matcher.topic)

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
            for listener in self._iter_matching_listeners(message.topic):
                try:
                    listener(payload, message.timestamp)
                except Exception:       # pylint: disable=W0703
                    logging.exception('Handling MQTT message')
                    sys.exit(1)
        except KeyError:
            logging.exception('_on_message')

    def _topic(self, *p):
        if not p[0]:
            return None
        return os.path.join(self._topic_prefix, *p)

    def _iter_matching_listeners(self, topic):
        for matcher, listeners in self._subscribe_map.items():
            if matcher.match(topic):
                yield from listeners

    def subscribe(self, topic, on_payload):
        topic = self._topic(topic)
        matcher = TopicMatcher(topic)
        if topic not in self._subscribe_map:
            self._subscribe_map[matcher] = []
        self._subscribe_map[matcher].append(on_payload)

    def publish(self, topic, payload, retain=False, qos=0):
        if not topic:
            logging.warning('Ignoring empty topic')
            return
        topic = self._topic(topic)
        logging.debug("Publish %s: %s", topic, payload)
        try:
            self._client.publish(topic, payload=payload, qos=qos, retain=retain)
        except TypeError as ex:
            logging.error('%s Value "%s" is a %s', ex, payload, type(payload))


class TopicMatcher:
    plus_pattern = r'(?:^|(?<=/))\+(?:$|(?=/))'  # find all `+` symbols like `+/...`, `.../+/...`, `.../+`
    hash_pattern = r'(?:^|(?<=/))#$'  # find all `#` symbols like `#`, `.../#`

    def __init__(self, topic):
        self._topic = topic
        self._re = self._topic_to_regex(topic)

    def __hash__(self):
        return hash(self._topic)

    @property
    def topic(self):
        return self._topic

    def match(self, topic):
        if self._re:
            try:
                return self._re.match(topic) is not None
            except re.error as ex:
                logging.error('Matching topic: %s because %s: %s', topic, ex.__class__.__name__, ex)
        return self._topic == topic

    @classmethod
    def _topic_to_regex(cls, topic):
        re_topic = topic
        try:
            if re.search(cls.plus_pattern, topic):
                re_topic = re.sub(cls.plus_pattern, '[^/]+', re_topic)
            if re.search(cls.hash_pattern, topic):
                re_topic = re.sub(cls.hash_pattern, '.+$', re_topic)
            if '#' in re_topic:
                logging.warning("Bad MQTT topic pattern, unexpected '#': %s", topic)
                return None
            if re_topic != topic:
                return re.compile(re_topic)
        except re.error:
            logging.warning('Bad MQTT topic pattern, could not parse: %s', topic)
        return None
