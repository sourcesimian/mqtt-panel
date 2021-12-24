import json
import logging

import geventwebsocket.exceptions

from mqtt_panel.web.widget.widget import Widget


class WSHandler:
    def __init__(self, service, session, ws, client_env, app_identity):
        self._service = service
        self._session = session
        self._ws = ws
        self.client_id = f'{client_env["REMOTE_ADDR"]}:{client_env["REMOTE_PORT"]}'
        self._app_identity = app_identity
        self._active_widgets = []

    def handle(self):
        logging.debug('(%s) Connect', self.client_id)
        self.send_app_info()

        while not self._ws.closed:
            rx = self._ws.receive()
            if not rx:
                continue
            logging.debug('(%s) Rx: %s', self.client_id, rx)
            blob_list = json.loads(rx)
            for blob in blob_list:
                try:
                    blob_id = blob['id']
                    if blob_id == 'register':
                        self.register(blob['widgets'])
                    elif blob_id.startswith(Widget._id_prefix):
                        widget = self._service._widget_store.get_widget(blob_id)
                        if not widget:
                            continue
                        widget.on_widget(blob)
                        # self._send([{'id': 'keepalive'}])
                        # if widget.on_widget(blob):
                        #     self._service.notify_all([widget.blob()])
                        # else:
                        #     self._send(widget.blob())
                except Exception:       # pylint: disable=W0703
                    logging.exception('(%s) Handling message blob "%s"', self.client_id, blob)
        logging.debug('(%s) Disconnect', self.client_id)

    def register(self, widgets):
        self._active_widgets = widgets

        blob_list = [w.blob() for w in self._service._widget_store if w.id in self._active_widgets]
        self._send(blob_list)

    def send(self, data):
        if not self._session.authorized:
            data = [{
                'id': 'app',
                'action': 'disconnect'
            }]
            self._send(data)
            self._ws.close()
            return

        filtered_data = []
        for blob in data:
            if blob['id'].startswith(Widget._id_prefix):
                if blob['id'] in self._active_widgets:
                    filtered_data.append(blob)
            else:
                filtered_data.append(blob)
        self._send(filtered_data)

    def _send(self, data):
        if not data:
            return
        message = json.dumps(data)
        logging.debug('(%s) Tx: %s', self.client_id, message)

        try:
            self._ws.send(message)
        except geventwebsocket.exceptions.WebSocketError as ex:
            logging.error('(%s) Tx Error: %s: %s', self.client_id, ex.__class__.__name__, ex)

    def send_app_info(self):
        data = {
            'id': 'app',
            'mqttOnline': self._service._mqtt_online,
            'appIdentity': self._app_identity,
        }
        self.send([data])
