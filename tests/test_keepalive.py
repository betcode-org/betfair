import unittest
import mock

from tests.tools import create_mock_json
from betfairlightweight.endpoints.keepalive import KeepAlive
from betfairlightweight import APIClient
from betfairlightweight.exceptions import KeepAliveError


class KeepAliveTest(unittest.TestCase):

    def setUp(self):
        client = APIClient('username', 'password', 'app_key', 'UK')
        self.keep_alive = KeepAlive(client)

    @mock.patch('betfairlightweight.endpoints.keepalive.KeepAlive.request')
    def test_call(self, mock_response):
        mock = create_mock_json('tests/resources/keep_alive_success.json')
        mock_response.return_value = mock
        response = self.keep_alive()

        assert response == mock.json()
        assert self.keep_alive.client.session_token == mock.json().get('token')

    @mock.patch('betfairlightweight.baseclient.BaseClient.cert')
    @mock.patch('betfairlightweight.baseclient.BaseClient.keep_alive_headers')
    @mock.patch('betfairlightweight.baseclient.requests.post')
    def test_request(self, mock_post, mock_keep_alive_headers, mock_cert):
        mock_response = create_mock_json('tests/resources/logout_success.json')
        mock_post.return_value = mock_response

        mock_headers = mock.Mock()
        mock_headers.return_value = {}
        mock_keep_alive_headers.return_value = mock_headers

        mock_client_cert = mock.Mock()
        mock_client_cert.return_value = []
        mock_cert.return_value = mock_client_cert

        url = 'https://identitysso.betfair.com/api/keepAlive'
        response = self.keep_alive.request()

        mock_post.assert_called_once_with(url, headers=mock_keep_alive_headers, cert=mock_cert)
        assert response == mock_response

    def test_keep_alive_error_handler(self):
        mock_response = create_mock_json('tests/resources/keep_alive_success.json')
        assert self.keep_alive._error_handler(mock_response.json()) is None

        mock_response = create_mock_json('tests/resources/keep_alive_fail.json')
        with self.assertRaises(KeepAliveError):
            self.keep_alive._error_handler(mock_response.json())

    def test_url(self):
        assert self.keep_alive.url == 'https://identitysso.betfair.com/api/keepAlive'
