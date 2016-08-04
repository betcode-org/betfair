import unittest
import mock
from requests.exceptions import ConnectionError

from tests.tools import create_mock_json
from betfairlightweight import APIClient
from betfairlightweight.endpoints.navigation import Navigation
from betfairlightweight.exceptions import APIError


class NavigationInit(unittest.TestCase):

    def test_base_endpoint_init(self):
        client = APIClient('username', 'password', 'app_key')
        navigation = Navigation(client)
        assert navigation.timeout == 3.05
        assert navigation._error == APIError
        assert navigation.client == client


class NavigationTest(unittest.TestCase):

    def setUp(self):
        client = APIClient('username', 'password', 'app_key', 'UK')
        self.navigation = Navigation(client)

    @mock.patch('betfairlightweight.endpoints.navigation.Navigation.request')
    def test_list_navigation(self, mock_response):
        mock_response.return_value = None
        response = self.navigation.list_navigation()
        assert response == mock_response()

    @mock.patch('betfairlightweight.baseclient.BaseClient.cert')
    @mock.patch('betfairlightweight.baseclient.BaseClient.request_headers')
    @mock.patch('betfairlightweight.baseclient.requests.get')
    def test_request(self, mock_get, mock_request_headers, mock_cert):
        mock_response = create_mock_json('tests/resources/login_success.json')
        mock_get.return_value = mock_response

        mock_headers = mock.Mock()
        mock_headers.return_value = {}
        mock_request_headers.return_value = mock_headers

        mock_client_cert = mock.Mock()
        mock_client_cert.return_value = []
        mock_cert.return_value = mock_client_cert

        url = 'https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json'
        self.navigation.request()

        mock_get.assert_called_once_with(url, headers=mock_request_headers, timeout=(3.05, 12))

    @mock.patch('betfairlightweight.baseclient.BaseClient.cert')
    @mock.patch('betfairlightweight.baseclient.BaseClient.request_headers')
    @mock.patch('betfairlightweight.baseclient.requests.get')
    def test_request_error(self, mock_get, mock_request_headers, mock_cert):
        mock_get.side_effect = ConnectionError()

        mock_headers = mock.Mock()
        mock_headers.return_value = {}
        mock_request_headers.return_value = mock_headers

        mock_client_cert = mock.Mock()
        mock_client_cert.return_value = []
        mock_cert.return_value = mock_client_cert

        url = 'https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json'
        with self.assertRaises(APIError):
            self.navigation.request()

        mock_get.assert_called_once_with(url, headers=mock_request_headers, timeout=(3.05, 12))

    @mock.patch('betfairlightweight.baseclient.BaseClient.cert')
    @mock.patch('betfairlightweight.baseclient.BaseClient.request_headers')
    @mock.patch('betfairlightweight.baseclient.requests.get')
    def test_request_random(self, mock_get, mock_request_headers, mock_cert):
        mock_get.side_effect = ValueError()

        mock_headers = mock.Mock()
        mock_headers.return_value = {}
        mock_request_headers.return_value = mock_headers

        mock_client_cert = mock.Mock()
        mock_client_cert.return_value = []
        mock_cert.return_value = mock_client_cert

        url = 'https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json'
        with self.assertRaises(APIError):
            self.navigation.request()

        mock_get.assert_called_once_with(url, headers=mock_request_headers, timeout=(3.05, 12))

    def test_url(self):
        assert self.navigation.url == self.navigation.client.navigation_uri
