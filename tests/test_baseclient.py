import datetime
import unittest

from betfairlightweight import APIClient
from betfairlightweight.exceptions import AppKeyError


class BaseClientInit(unittest.TestCase):

    def test_base_client_init(self):
        client = APIClient('username', 'password', 'app_key')
        assert client.username == 'username'
        assert client.password == 'password'
        assert client.app_key == 'app_key'
        assert client._login_time is None
        assert client.session_token is None

    def test_uri(self):
        client = APIClient('username', 'password', 'app_key')
        assert client.locale is None
        assert client.identity_uri == 'https://identitysso.betfair.com/api/'
        assert client.api_uri == 'https://api.betfair.com/exchange/betting/json-rpc/v1'

        client = APIClient('username', 'password', 'app_key', 'australia')
        assert client.locale == 'australia'
        assert client.identity_uri == 'https://identitysso.betfair.com/api/'
        assert client.api_uri == 'https://api-au.betfair.com/exchange/betting/json-rpc/v1'

        client = APIClient('username', 'password', 'app_key', 'spain')
        assert client.locale == 'spain'
        assert client.identity_uri == 'https://identitysso.betfair.es'
        assert client.api_uri == 'https://api.betfair.com/exchange/betting/json-rpc/v1'

        client = APIClient('username', 'password', 'app_key', 'italy')
        assert client.locale == 'italy'
        assert client.identity_uri == 'https://identitysso.betfair.it/api/'
        assert client.api_uri == 'https://api.betfair.com/exchange/betting/json-rpc/v1'

        client = APIClient('username', 'password', 'app_key', 'romania')
        assert client.locale == 'romania'
        assert client.identity_uri == 'https://idenititysso.betfair.ro'
        assert client.api_uri == 'https://api.betfair.com/exchange/betting/json-rpc/v1'

        client = APIClient('username', 'password', 'app_key', 'w_con')
        assert client.locale == 'w_con'
        assert client.identity_uri == 'https://identitysso.w-con.betfair.com'
        assert client.api_uri == 'https://api.betfair.com/exchange/betting/json-rpc/v1'

        client = APIClient('username', 'password', 'app_key', 'europe')
        assert client.locale == 'europe'
        assert client.identity_uri == 'https://identitysso.betfaironline.eu'
        assert client.api_uri == 'https://api.betfair.com/exchange/betting/json-rpc/v1'


class BaseClientTest(unittest.TestCase):

    def setUp(self):
        self.client = APIClient('username', 'password', 'app_key')

    def test_client_certs(self):
        # assert client.cert == ['/certs/client-2048.crt', '/certs/client-2048.key']  # fails travis
        pass

    def test_set_session_token(self):
        self.client.set_session_token('session_token')
        assert self.client.session_token == 'session_token'
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
        self.client.set_session_token('session_token')

        assert self.client.session_expired is None
        self.client._login_time = datetime.datetime(2003, 8, 4, 12, 30, 45)
        assert self.client.session_expired is True

    def test_client_logout(self):
        self.client.client_logout()
        assert self.client._login_time is None
        assert self.client.session_token is None
