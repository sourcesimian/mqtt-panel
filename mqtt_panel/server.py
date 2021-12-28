import io
import json
import logging
import urllib

import gevent.pool
import gevent.server
import gevent.socket
import gevent.pywsgi

from geventwebsocket.handler import WebSocketHandler

from mqtt_panel.session import Session


class Server:
    def __init__(self, binding, config, auth):
        self._server = None
        self._c = config
        self._auth = auth
        self._binding = binding
        log_level = self._c.get('log-level', None)
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
                self._binding.websocket(session, env["wsgi.websocket"], env)
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

        if path == ('style.css',):
            start_response('200 OK', [('Content-Type', 'text/css')])
            with open('./resources/style.css', encoding="utf8") as fh:
                return [fh.read().encode()]

        start_response('404 Not Found', [('Content-Type', 'text/html')])
        return [b'<h1>Not Found</h1>']
