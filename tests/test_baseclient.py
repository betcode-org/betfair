import datetime
import unittest
import mock

from betfairlightweight import APIClient
from betfairlightweight.exceptions import AppKeyError, CertsError


class BaseClientInit(unittest.TestCase):

    def test_base_client_init(self):
        client = APIClient('username', 'password', 'app_key')
        assert client.username == 'username'
        assert client.password == 'password'
        assert client.app_key == 'app_key'
        assert client.certs is None
        assert client.locale is None
        assert client._login_time is None
        assert client.session_token is None

    def test_uri(self):
        client = APIClient('username', 'password', 'app_key')
        assert client.locale is None
        assert client.identity_uri == 'https://identitysso.betfair.com/api/'
        assert client.api_uri == 'https://api.betfair.com/exchange/'
        assert client.navigation_uri == 'https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json'

        client = APIClient('username', 'password', 'app_key', locale='australia')
        assert client.locale == 'australia'
        assert client.identity_uri == 'https://identitysso.betfair.com/api/'
        assert client.api_uri == 'https://api-au.betfair.com/exchange/'
        assert client.navigation_uri == 'https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json'

        client = APIClient('username', 'password', 'app_key', locale='spain')
        assert client.locale == 'spain'
        assert client.identity_uri == 'https://identitysso.betfair.es'
        assert client.api_uri == 'https://api.betfair.com/exchange/'
        assert client.navigation_uri == 'https://api.betfair.es/exchange/betting/rest/v1/en/navigation/menu.json'

        client = APIClient('username', 'password', 'app_key', locale='italy')
        assert client.locale == 'italy'
        assert client.identity_uri == 'https://identitysso.betfair.it/api/'
        assert client.api_uri == 'https://api.betfair.com/exchange/'
        assert client.navigation_uri == 'https://api.betfair.it/exchange/betting/rest/v1/en/navigation/menu.json'

        client = APIClient('username', 'password', 'app_key', locale='romania')
        assert client.locale == 'romania'
        assert client.identity_uri == 'https://idenititysso.betfair.ro'
        assert client.api_uri == 'https://api.betfair.com/exchange/'
        assert client.navigation_uri == 'https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json'

        client = APIClient('username', 'password', 'app_key', locale='w_con')
        assert client.locale == 'w_con'
        assert client.identity_uri == 'https://identitysso.w-con.betfair.com'
        assert client.api_uri == 'https://api.betfair.com/exchange/'
        assert client.navigation_uri == 'https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json'

        client = APIClient('username', 'password', 'app_key', locale='europe')
        assert client.locale == 'europe'
        assert client.identity_uri == 'https://identitysso.betfaironline.eu'
        assert client.api_uri == 'https://api.betfair.com/exchange/'
        assert client.navigation_uri == 'https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json'


class BaseClientTest(unittest.TestCase):

    def setUp(self):
        self.client = APIClient('username', 'password', 'app_key', '/fail/')

    def test_client_certs(self):
        with self.assertRaises(CertsError):
            print(self.client.cert)

    @mock.patch('betfairlightweight.baseclient.os.listdir')
    def test_client_certs_mocked(self, mock_listdir):
        mock_listdir.return_value = ['.DS_Store', 'client-2048.crt', 'client-2048.key']
        assert self.client.cert == ['/fail/client-2048.crt', '/fail/client-2048.key']

    def test_set_session_token(self):
        self.client.set_session_token('session_token')
        assert self.client.session_token == 'session_token'
        assert self.client._login_time is not None

    def test_get_app_key(self):
        self.client.app_key = None
        with self.assertRaises(AppKeyError):
            self.client.get_app_key()
        self.client.app_key = 'app_key'

    @mock.patch('betfairlightweight.baseclient.os.environ')
    def test_get_app_key_mocked(self, mocked_environ):
        self.client.app_key = None
        mocked_environ.__get__ = mock.Mock(return_value='app_key')
        assert self.client.get_app_key() is None

    def test_client_headers(self):
        assert self.client.login_headers == {'X-Application': '1',
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
