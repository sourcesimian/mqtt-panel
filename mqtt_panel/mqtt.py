import logging
import os.path
import paho.mqtt.client

import gevent

class Mqtt(object):
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
        self._client.on_message=self._on_message 

        connect = {
            'host': self._c.get('host', 'localhost'),
            'port': self._c.get('port', 1833),
        }
        self._client.connect(**connect)
        
    def _on_connect(self, client, userdata, flags, rc):
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
            except Exception as ex:
                logging.error('Run loop exception %s: %s', ex.__class__.__name__, ex)
                gevent.sleep(10)

    def close(self):
        logging.info("Close")
        if self._client:
            client = self._client
            self._client = None
            client.disconnect()

    def _on_disconnect(self, client, userdata, rc):
        logging.info("On Disconnect")
        self._notify_watchers(False)

        if self._client:
            self.close()
            self.open()

    def _on_message(self, client, userdata, message):
        if self._topic_prefix and not message.topic.startswith(self._topic_prefix):
            logging.warning('Dropped message: %s', message)
            return

        try:
            payload = message.payload.decode()
            retained = ' (retained)' if message.retain else ''
            logging.info("Received %s: %s%s", message.topic, payload, retained)
            for listener in self._subscribe_map[message.topic]:
                try:
                    listener(payload, message.timestamp)
                except Exception as ex:
                    logging.exception('Handling MQTT message')
                    exit(1)
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
        topic = self._topic(topic)
        logging.debug("Publish %s: %s", topic, payload)
        self._client.publish(topic, payload=payload, qos=qos, retain=retain)
