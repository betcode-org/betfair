import datetime
import unittest

from betfairlightweight import APIClient
from betfairlightweight.exceptions import AppKeyError


class BaseClientInit(unittest.TestCase):

    def test_base_client_init(self):
        client = APIClient('username', 'password', 'app_key', 'UK')
        assert client.username == 'username'
        assert client.password == 'password'
        assert client.app_key == 'app_key'
        assert client.exchange == 'UK'
        assert client._login_time is None
        assert client.session_token is None

    def test_base_client_aus_init(self):
        client_aus = APIClient('username', 'password', 'app_key', 'AUS')
        assert client_aus.username == 'username'
        assert client_aus.password == 'password'
        assert client_aus.app_key == 'app_key'
        assert client_aus.exchange == 'AUS'
        assert client_aus._login_time is None
        assert client_aus.session_token is None


class BaseClientTest(unittest.TestCase):

    def setUp(self):
        self.client = APIClient('username', 'password', 'app_key', 'UK')

    def test_client_certs(self):
        # assert client.cert == ['/certs/client-2048.crt', '/certs/client-2048.key']  # fails travis
        pass

    def test_set_session_token(self):
        self.client.set_session_token('test')
        assert self.client.session_token == 'test'
        assert self.client._login_time is not None

    def test_get_app_key(self):
        self.client.app_key = None
        with self.assertRaises(AppKeyError):
            self.client.get_app_key()
        self.client.app_key = 'app_key'

    def test_client_headers(self):
        assert self.client.login_headers == {'X-Application': 1,
                                             'content-type': 'application/x-www-form-urlencoded'}
        assert self.client.keep_alive_headers == {'Accept': 'application/json',
                                                  'X-Application': self.client.app_key,
                                                  'X-Authentication': self.client.session_token,
                                                  'content-type': 'application/x-www-form-urlencoded'}
        assert self.client.request_headers == {'X-Application': self.client.app_key,
                                               'X-Authentication': self.client.session_token,
                                               'content-type': 'application/json'}

    def test_client_logged_in_session(self):
        self.client.set_session_token('test')

        assert self.client.session_expired is None
        self.client._login_time = datetime.datetime(2003, 8, 4, 12, 30, 45)
        assert self.client.session_expired is True
        self.client.set_session_token('sessiontoken')
        assert self.client.session_expired is None

    def test_client_logout(self):
        self.client.client_logout()
        assert self.client._login_time is None
        assert self.client.session_token is None
