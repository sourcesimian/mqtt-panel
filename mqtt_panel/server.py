import io
import json
import logging
import os
import urllib

import gevent.pool
import gevent.server
import gevent.socket
import gevent.pywsgi

from geventwebsocket.handler import WebSocketHandler

from mqtt_panel.session import Session


ext_map = {
    'jquery.js': {
        'Content-Type': "application/javascript",
        'url': "https://code.jquery.com/jquery-1.11.1.min.js"
    },
    'jquery.mobile.js': {
        'Content-Type': "application/javascript",
        'url': "https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.js"
    },
    'bootstrap.css': {
        'Content-Type': "text/css",
        'url': "https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"
    },
    'material-icons.css': {
        'Content-Type': "text/css",
        'url': "https://fonts.googleapis.com/icon?family=Material+Icons"
    },
    'material-icons.ttf': {
        'Content-Type': "font/ttf",
        'url': "https://fonts.gstatic.com/s/materialicons/v139/flUhRq6tzZclQEJ-Vdg-IuiaDsNZ.ttf"
    },
}

class Server:
    def __init__(self, binding, config, auth):
        self._server = None
        self._c = config
        self._auth = auth
        self._binding = binding
        log_level = self._c.get('logging-level', None)
        if log_level:
            logging.getLogger('geventwebsocket.handler').setLevel(log_level)

    def open(self):
        logging.info('Open')
        pool = gevent.pool.Pool(self._c.get('max-connections', 100))
        bind = (
            self._c.get('bind', '0.0.0.0'),
            int(self._c.get('port', 8080))
        )
        logging.info('Server listening on: %s:%s', *bind)
        self._server = gevent.pywsgi.WSGIServer(
            bind,
            self._handle_request,
            handler_class=WebSocketHandler,
            spawn=pool)
        try:
            self._server.start()
            return True
        except OSError as ex:
            logging.error('%s: %s', ex.__class__.__name__, ex)
        return False

    def close(self):
        logging.info('Close')
        self._server.stop()
        self._server = None

    def _handle_request(self, env, start_response):  # pylint: disable=R0911,R0912,R0915
        path = tuple(env["PATH_INFO"].split('/'))[1:]

        session = Session(self._auth)
        session.from_cookie(env.get('HTTP_COOKIE', None))

        if path == ('',):
            # Login
            if not session.authorized:
                start_response('200 OK', [
                    ('Content-Type', 'text/html'),
                    ('Content-Language', 'us-GB'),
                ])
                out = io.StringIO()
                self._binding.login(out)
                return [out.getvalue().encode()]

            # App
            start_response('200 OK', [
                ('Content-Type', 'text/html'),
                ('Content-Language', 'us-GB'),
            ])
            out = io.StringIO()
            self._binding.app(out)
            return [out.getvalue().encode()]

        if path == ('api', 'login'):
            content = env['wsgi.input'].read().decode()
            query = urllib.parse.parse_qs(content)

            success = False
            message = "Bad username or password"
            if 'username' in query:
                try:
                    success = session.login(query['username'][0], query['password'][0])
                except (KeyError, IndexError):
                    pass
                if success:
                    message = "Success"
            start_response('200 OK', [
                ('Content-Type', 'application/json'),
                ('Set-Cookie', session.as_cookie()),
            ])
            ret = {
                'session': session.as_cookie(),
                'success': success,
                'message': message,
            }
            return [json.dumps(ret).encode()]

        if path == ('api', 'logout'):
            session.logout()
            start_response('200 OK', [
                ('Content-Type', 'application/json'),
                ('Set-Cookie', session.as_cookie()),
            ])
            ret = {
                'session': session.as_cookie()
            }
            return [json.dumps(ret).encode()]

        if path == ('ws',):
            if env.get('HTTP_UPGRADE', None) == 'websocket':
                self._binding.web_socket(session, env["wsgi.websocket"], env)
                return []
            start_response('400 Bad Request', [('Content-Type', 'text/html')])
            return [b'<h1>Bad Request</h1>']

        if path == ('api', 'health',):
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [json.dumps({'health': 'okay'}).encode()]

        if path == ('icon-192x192.png',):
            start_response('200 OK', [('Content-Type', 'image/png')])
            with open('./resources/icon-192x192.png', 'rb') as fh:
                return [fh.read()]

        if path == ('ios-icon-192x192.png',):
            start_response('200 OK', [('Content-Type', 'image/png')])
            with open('./resources/ios-icon-192x192.png', 'rb') as fh:
                return [fh.read()]

        if path == ('favicon.ico',):
            start_response('200 OK', [('Content-Type', 'image/x-icon')])
            with open('./resources/favicon.ico', 'rb') as fh:
                return [fh.read()]

        if path == ('manifest.json',):
            start_response('200 OK', [('Content-Type', 'application/json')])
            with open('./resources/manifest.json', encoding="utf8") as fh:
                return [fh.read().encode()]

        if path[0] == 'ext':
            if path[1] in ext_map:
                start_response('200 OK', [('Content-Type', ext_map[path[1]]['Content-Type'])])
                if not os.path.exists('./ext'):
                    os.makedirs('./ext')
                local_file = './ext/%s' % path[1]
                if not os.path.exists(local_file):
                    import requests
                    with open(local_file, mode="wb") as fh:
                        fh.write(requests.get(ext_map[path[1]]['url']).content)

                with open(local_file, mode="rb") as fh:
                    return [fh.read()]

        start_response('404 Not Found', [('Content-Type', 'text/html')])
        return [b'<h1>Not Found</h1>']
