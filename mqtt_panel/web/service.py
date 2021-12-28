import logging

from mqtt_panel.web.wshandler import WSHandler


class Service:
    def __init__(self, widget_store):
        self._mqtt_online = False
        self._widget_store = widget_store
        self._web_sockets = {}

        for widget in self._widget_store:
            widget.set_update_widget(self._notify_all)

    def get_widget(self, widget_id):
        return self._widget_store.get_widget(widget_id)

    def get_blob_list(self, active_widgets):
        return [w.blob() for w in self._widget_store if w.id in active_widgets]

    def _notify_all(self, blob):
        self.notify_all([blob])

    def web_socket(self, session, ws, client_env, app_identity):
        wsh = WSHandler(self, session, ws, client_env, app_identity)
        self._web_sockets[wsh.client_id] = wsh

        try:
            wsh.handle()
        except Exception:  # pylint: disable=W0703
            logging.exception('(%s) Web socket handler', wsh.client_id)
        finally:
            del self._web_sockets[wsh.client_id]

    def set_mqtt_online(self, online):
        logging.debug("MQTT online status:%s", online)
        self._mqtt_online = online
        for _client_id, wsh in self._web_sockets.items():
            wsh.send_app_info()

    @property
    def mqtt_online(self):
        return self._mqtt_online

    def notify_all(self, blob):
        for _client_id, wsh in self._web_sockets.items():
            wsh.send(blob)
