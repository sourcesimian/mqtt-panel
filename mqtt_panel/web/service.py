import logging

from mqtt_panel.web.wshandler import WSHandler


class Service(object):
    def __init__(self, widget_store):
        self._mqtt_online = False
        self._widget_store = widget_store
        self._web_sockets = {}

        for widget in self._widget_store:
            widget.set_update_widget(self._notify_all)

    def _notify_all(self, blob):
        self.notify_all([blob])

    def web_socket(self, session, ws, client_env, app_identity):
        wsh = WSHandler(self, session, ws, client_env, app_identity)
        self._web_sockets[wsh.client_id] = wsh

        try:
            wsh.handle()
        except Exception as ex:
            logging.exception('(%s) Web socket handler', wsh.client_id)
        finally:
            del self._web_sockets[wsh.client_id]

    def mqtt_online(self, online):
        logging.debug("MQTT online status:%s", online)
        self._mqtt_online = online
        for client_id, wsh in self._web_sockets.items():
            wsh.send_app_info()

    def notify_all(self, blob):
        for client_id, wsh in self._web_sockets.items():
            wsh.send(blob)
