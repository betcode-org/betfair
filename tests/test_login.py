import unittest
import mock
from requests.exceptions import ConnectionError

from tests.tools import create_mock_json
from betfairlightweight.endpoints.login import Login
from betfairlightweight import APIClient
from betfairlightweight.exceptions import LoginError, APIError


class LoginTest(unittest.TestCase):

    def setUp(self):
        client = APIClient('username', 'password', 'app_key', 'UK')
        self.login = Login(client)

    @mock.patch('betfairlightweight.endpoints.login.Login.request')
    def test_call(self, mock_response):
        mock = create_mock_json('tests/resources/login_success.json')
        mock_response.return_value = mock
        response = self.login()

        assert response == mock.json()
        assert self.login.client.session_token == mock.json().get('sessionToken')

    @mock.patch('betfairlightweight.baseclient.BaseClient.cert')
    @mock.patch('betfairlightweight.baseclient.BaseClient.login_headers')
    @mock.patch('betfairlightweight.baseclient.requests.post')
    def test_request(self, mock_post, mock_login_headers, mock_cert):
        mock_response = create_mock_json('tests/resources/login_success.json')
        mock_post.return_value = mock_response

        mock_headers = mock.Mock()
        mock_headers.return_value = {}
        mock_login_headers.return_value = mock_headers

        mock_client_cert = mock.Mock()
        mock_client_cert.return_value = []
        mock_cert.return_value = mock_client_cert

        url = 'https://identitysso.betfair.com/api/certlogin'
        response = self.login.request()

        mock_post.assert_called_once_with(url, data='username=username&password=password',
                                          headers=mock_login_headers, cert=mock_cert)
        assert response == mock_response

    @mock.patch('betfairlightweight.baseclient.BaseClient.cert')
    @mock.patch('betfairlightweight.baseclient.BaseClient.login_headers')
    @mock.patch('betfairlightweight.utils.check_status_code')
    @mock.patch('betfairlightweight.baseclient.requests.post')
    def test_request_error(self, mock_post, mock_check, mock_login_headers, mock_cert):
        mock_post.side_effect = ConnectionError()
        mock_check.return_value = None
        mock_headers = mock.Mock()
        mock_headers.return_value = {}
        mock_login_headers.return_value = mock_headers

        mock_client_cert = mock.Mock()
        mock_client_cert.return_value = []
        mock_cert.return_value = mock_client_cert

        url = 'https://identitysso.betfair.com/api/certlogin'
        with self.assertRaises(APIError):
            self.login.request()

        mock_post.assert_called_once_with(url, data='username=username&password=password',
                                          headers=mock_login_headers, cert=mock_cert)

    @mock.patch('betfairlightweight.baseclient.BaseClient.cert')
    @mock.patch('betfairlightweight.baseclient.BaseClient.login_headers')
    @mock.patch('betfairlightweight.utils.check_status_code')
    @mock.patch('betfairlightweight.baseclient.requests.post')
    def test_request_error_random(self, mock_post, mock_check, mock_login_headers, mock_cert):
        mock_post.side_effect = ValueError()
        mock_check.return_value = None
        mock_headers = mock.Mock()
        mock_headers.return_value = {}
        mock_login_headers.return_value = mock_headers

        mock_client_cert = mock.Mock()
        mock_client_cert.return_value = []
        mock_cert.return_value = mock_client_cert

        url = 'https://identitysso.betfair.com/api/certlogin'
        with self.assertRaises(APIError):
            self.login.request()

        mock_post.assert_called_once_with(url, data='username=username&password=password',
                                          headers=mock_login_headers, cert=mock_cert)

    def test_login_error_handler(self):
        mock_response = create_mock_json('tests/resources/login_success.json')
        assert self.login._error_handler(mock_response.json()) is None

        mock_response = create_mock_json('tests/resources/login_fail.json')
        with self.assertRaises(LoginError):
            self.login._error_handler(mock_response.json())

    def test_url(self):
        assert self.login.url == 'https://identitysso.betfair.com/api/certlogin'

    def test_data(self):
        assert self.login.data == 'username=username&password=password'
