import os
import unittest
from unittest import mock

from betfairlightweight.baseclient import IDENTITY, IDENTITY_CERT, API, NAVIGATION
from betfairlightweight import APIClient
from betfairlightweight.exceptions import PasswordError, AppKeyError, CertsError


class BaseClientInit(unittest.TestCase):
    def test_base_client_init(self):
        client = APIClient("bf_username", "password", "app_key", lightweight=True)
        assert client.username == "bf_username"
        assert client.password == "password"
        assert client.app_key == "app_key"
        assert client.lightweight is True
        assert client.certs is None
        assert client.locale is None
        assert client._login_time is None
        assert client.session_token is None

    def test_vars(self):
        assert IDENTITY == "https://identitysso.betfair{tld}/api/"
        assert IDENTITY_CERT == "https://identitysso-cert.betfair{tld}/api/"
        assert API == "https://api.betfair.com/exchange/"
        assert (
            NAVIGATION
            == "https://api.betfair{tld}/exchange/betting/rest/v1/{locale}/navigation/menu.json"
        )

    def test_uri(self):
        client = APIClient("bf_username", "password", "app_key")
        assert client.locale is None
        assert client.identity_uri == "https://identitysso.betfair.com/api/"
        assert client.api_uri == "https://api.betfair.com/exchange/"
        assert (
            client.navigation_uri
            == "https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json"
        )
        assert client.identity_cert_uri == "https://identitysso-cert.betfair.com/api/"

        client = APIClient("bf_username", "password", "app_key", locale="australia")
        assert client.locale == "australia"
        assert client.identity_uri == "https://identitysso.betfair.com.au/api/"
        assert client.api_uri == "https://api.betfair.com/exchange/"
        assert (
            client.navigation_uri
            == "https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json"
        )
        assert client.identity_cert_uri == "https://identitysso-cert.betfair.com/api/"

        client = APIClient("bf_username", "password", "app_key", locale="spain")
        assert client.locale == "spain"
        assert client.identity_uri == "https://identitysso.betfair.es/api/"
        assert client.api_uri == "https://api.betfair.com/exchange/"
        assert (
            client.navigation_uri
            == "https://api.betfair.es/exchange/betting/rest/v1/es/navigation/menu.json"
        )
        assert client.identity_cert_uri == "https://identitysso-cert.betfair.es/api/"

        client = APIClient("bf_username", "password", "app_key", locale="italy")
        assert client.locale == "italy"
        assert client.identity_uri == "https://identitysso.betfair.it/api/"
        assert client.api_uri == "https://api.betfair.com/exchange/"
        assert (
            client.navigation_uri
            == "https://api.betfair.it/exchange/betting/rest/v1/it/navigation/menu.json"
        )
        assert client.identity_cert_uri == "https://identitysso-cert.betfair.it/api/"

        client = APIClient("bf_username", "password", "app_key", locale="romania")
        assert client.locale == "romania"
        assert client.identity_uri == "https://identitysso.betfair.ro/api/"
        assert client.api_uri == "https://api.betfair.com/exchange/"
        assert (
            client.navigation_uri
            == "https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json"
        )
        assert client.identity_cert_uri == "https://identitysso-cert.betfair.ro/api/"

        client = APIClient("bf_username", "password", "app_key", locale="sweden")
        assert client.locale == "sweden"
        assert client.identity_uri == "https://identitysso.betfair.se/api/"
        assert client.api_uri == "https://api.betfair.com/exchange/"
        assert (
            client.navigation_uri
            == "https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json"
        )
        assert client.identity_cert_uri == "https://identitysso-cert.betfair.se/api/"

    def test_session_timeout(self):
        client = APIClient("bf_username", "password", "app_key")
        assert client.session_timeout == 86400

        client = APIClient("bf_username", "password", "app_key", locale="italy")
        assert client.session_timeout == 1200


class BaseClientTest(unittest.TestCase):
    def setUp(self):
        self.client = APIClient("bf_username", "password", "app_key", "/fail/")

    def test_client_certs(self):
        with self.assertRaises(CertsError):
            print(self.client.cert)

    @mock.patch("betfairlightweight.baseclient.os.listdir")
    def test_client_certs_mocked(self, mock_listdir):
        mock_listdir.return_value = [".DS_Store", "client-2048.crt", "client-2048.key"]
        assert self.client.cert == ["/fail/client-2048.crt", "/fail/client-2048.key"]

    @mock.patch("betfairlightweight.baseclient.os.listdir")
    def test_client_certs_missing(self, mock_listdir):
        mock_listdir.return_value = [".DS_Store", "client-2048.key"]
        with self.assertRaises(CertsError):
            print(self.client.cert)

    def test_set_session_token(self):
        self.client.set_session_token("session_token")
        assert self.client.session_token == "session_token"
        assert self.client._login_time is not None

    def test_get_password(self):
        self.client.password = "test"
        assert self.client.get_password() == "test"

    def test_get_password_error(self):
        self.client.password = None
        with self.assertRaises(PasswordError):
            self.client.get_password()

    def test_get_app_key(self):
        self.client.app_key = "app_key"
        assert self.client.get_app_key() == "app_key"

    def test_get_app_key_error(self):
        self.client.app_key = None
        with self.assertRaises(AppKeyError):
            self.client.get_app_key()

    @mock.patch("betfairlightweight.baseclient.os.environ")
    def test_get_app_key_mocked(self, mocked_environ):
        self.client.app_key = None
        mocked_environ.__get__ = mock.Mock(return_value="app_key")
        self.assertEqual(self.client.get_app_key(), mocked_environ.get())

    @mock.patch("betfairlightweight.baseclient.USER_AGENT")
    def test_client_headers(self, mock_user_agent):
        assert self.client.login_headers == {
            "Accept": "application/json",
            "X-Application": self.client.app_key,
            "content-type": "application/x-www-form-urlencoded",
            "User-Agent": mock_user_agent,
        }
        assert self.client.keep_alive_headers == {
            "Accept": "application/json",
            "X-Application": self.client.app_key,
            "X-Authentication": self.client.session_token,
            "content-type": "application/x-www-form-urlencoded",
            "User-Agent": mock_user_agent,
        }
        assert self.client.request_headers == {
            "X-Application": self.client.app_key,
            "X-Authentication": self.client.session_token,
            "content-type": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "User-Agent": mock_user_agent,
        }

    def test_client_logged_in_session(self):
        assert self.client.session_expired is True
        self.client.set_session_token("session_token")
        assert self.client.session_expired is False
        self.client._login_time = 959814000
        assert self.client.session_expired is True

    def test_client_logout(self):
        self.client.client_logout()
        assert self.client._login_time is None
        assert self.client.session_token is None


def normpaths(p):
    return list(map(os.path.normpath, p))


class BaseClientRelativePathTest(unittest.TestCase):
    def setUp(self):
        self.client = APIClient(
            "bf_username", "password", "app_key", os.path.normpath("fail/")
        )

    @mock.patch("betfairlightweight.baseclient.os.listdir")
    def test_client_certs_mocked(self, mock_listdir):
        mock_listdir.return_value = normpaths(
            [".DS_Store", "client-2048.crt", "client-2048.key"]
        )
        assert self.client.cert == normpaths(
            ["../fail/client-2048.crt", "../fail/client-2048.key"]
        )


class BaseClientCertFilesTest(unittest.TestCase):
    def setUp(self):
        self.client = APIClient(
            "bf_username",
            "password",
            "app_key",
            cert_files=normpaths(["/fail/client-2048.crt", "/fail/client-2048.key"]),
        )

    def test_client_cert_files(self):
        assert self.client.cert == normpaths(
            ["/fail/client-2048.crt", "/fail/client-2048.key"]
        )
