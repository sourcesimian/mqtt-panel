import json
import http.cookies
import urllib.parse


class Session:
    _cookie_path = '/'
    _cookie_secure = False
    _cookie_ttl = 86400 * 365

    def __init__(self, auth):
        self._auth = auth
        self._session = None

    def from_cookie(self, cookie_str):
        if not cookie_str:
            return

        cookie = http.cookies.SimpleCookie(cookie_str)
        try:
            for key, morsel in cookie.items():
                if key == 'session':
                    self._session = json.loads(
                        urllib.parse.unquote(morsel.value, errors="strict"))
                    break
        except (ValueError, json.decoder.JSONDecodeError):
            pass

    @property
    def authorized(self):
        if not self._auth:
            return True
        try:
            if self._session['id'] != 'VALID':
                return False
            return True
        except (KeyError, TypeError):
            pass
        return False

    @property
    def username(self):
        try:
            return self._session['username']
        except KeyError:
            return None

    def login(self, username, password):
        for blob in self._auth.get('users', []):
            if blob.get('username', None) == username:
                if password == blob.get('password', None):
                    self._session = {
                        'username': username,
                        'id': 'VALID',
                    }
                    return True
        return False

    def logout(self):
        self._session = None

    def as_cookie(self):
        if self.authorized:
            return self._session_cookie()
        return self._deleted_cookie()

    def _session_cookie(self):
        session = http.cookies.Morsel()
        value = json.dumps(self._session)

        session.set('session', value, urllib.parse.quote(value))
        session['expires'] = self._cookie_ttl
        session['path'] = self._cookie_path
        # session['comment'] = 'foo'
        session['max-age'] = self._cookie_ttl
        session['secure'] = self._cookie_secure
        # session['version'] = 2
        # session['samesite'] = 2
        # session['httponly'] = False
        return session.output().split(': ', 1)[1]

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
        return session.output().split(': ', 1)[1]
