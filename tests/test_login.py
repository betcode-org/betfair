import unittest
import mock

from tests.tools import create_mock_json
from betfairlightweight.endpoints.login import Login
from betfairlightweight import APIClient
from betfairlightweight.exceptions import LoginError


class LoginTest(unittest.TestCase):

    def setUp(self):
        client = APIClient('username', 'password', 'app_key', 'UK')
        self.login = Login(client)

    def test_call(self):
        pass

    # @mock.patch('betfairlightweight.baseclient.BaseClient.cert')
    # @mock.patch('betfairlightweight.baseclient.BaseClient.login_headers')
    # @mock.patch('betfairlightweight.apiclient.requests.post')
    # def test_request(self, mock_post, mock_login_headers, mock_cert):
    #     mock_response = create_mock_json('tests/resources/login_success.json')
    #     mock_post.return_value = mock_response
    #
    #     mock_headers = mock.Mock()
    #     mock_headers.return_value = {}
    #     mock_login_headers.return_value = mock_headers
    #
    #     mock_client_cert = mock.Mock()
    #     mock_client_cert.return_value = []
    #     mock_cert.return_value = mock_client_cert
    #
    #     url = None
    #     response = self.login.request()
    #
    #     mock_post.assert_called_once_with(url, data=None, headers=mock_login_headers, cert=mock_cert)
    #     assert response == mock_response

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
