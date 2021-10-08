import json
import http.cookies
import urllib.parse


class Session(object):
    _cookie_path = '/'
    _cookie_secure = False

    def __init__(self):
        self._authorized = False
        self._cookie = None

    def from_cookie(self, cookie_str):
        if not cookie_str:
            return

        cookie = http.cookies.SimpleCookie(cookie_str)
        try:
            for key, morsel in cookie.items():
                if key == 'session':
                    self._cookie = json.loads(
                        urllib.parse.unquote(morsel.value, errors="strict"))
                    break
        except (ValueError, json.decoder.JSONDecodeError):
            pass

    @property
    def authorized(self):
        try:
            if self._cookie['id'] != 'authed':
                return False
            return True
        except (KeyError, TypeError):
            pass
        return False

    def login(self, user):
        self._cookie = {
            'id': 'authed'
        }

    def logout(self):
        self._cookie = None

    def as_cookie(self):
        if self.authorized:
            return self._session_cookie()
        else:
            return self._deleted_cookie()

    def _session_cookie(self):
        session = http.cookies.Morsel()
        value = json.dumps(self._cookie)
        ttl = 86400 * 365

        session.set('session', value, urllib.parse.quote(value))
        session['expires'] = ttl
        session['path'] = self._cookie_path
        # session['comment'] = 'foo'
        session['max-age'] = ttl
        session['secure'] = self._cookie_secure
        # session['version'] = 2
        # session['samesite'] = 2
        # session['httponly'] = False
        return session.output().split(': ', 1)

    def _deleted_cookie(self):
        session = http.cookies.Morsel()
        value = json.dumps({})
        ttl = 0

        session.set('session', value, urllib.parse.quote(value))
        session['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
        session['path'] = self._cookie_path
        # session['comment'] = 'foo'
        session['max-age'] = ttl
        session['secure'] = self._cookie_secure
        # session['version'] = 2
        # session['samesite'] = 2
        # session['httponly'] = False
        return session.output().split(': ', 1)
