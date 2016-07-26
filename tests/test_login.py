import unittest
import mock

from tests.tools import create_mock_json
from betfairlightweight.endpoints.login import Login
from betfairlightweight import APIClient


class LoginTest(unittest.TestCase):

    def setUp(self):
        client = APIClient('username', 'password', 'app_key', 'UK')
        self.login = Login(client)

    @mock.patch('betfairlightweight.endpoints.base.BaseEndpoint.create_resp')
    @mock.patch('betfairlightweight.baseclient.BaseClient.cert')
    @mock.patch('betfairlightweight.baseclient.BaseClient.login_headers')
    @mock.patch('betfairlightweight.apiclient.requests.post')
    def test_request(self, mock_post, mock_login_headers, mock_cert, mock_create_resp):
        mock_response = create_mock_json('resources/login_success.json')
        mock_post.return_value = mock_response

        mock_headers = mock.Mock()
        mock_headers.return_value = {}
        mock_login_headers.return_value = mock_headers

        mock_client_cert = mock.Mock()
        mock_client_cert.return_value = []
        mock_cert.return_value = mock_client_cert

        mock_create_response = mock.Mock()
        mock_create_response.return_value = (mock_post.json(), mock_response, None)
        mock_create_resp.return_value = mock_create_response

        url = 'http://api.empty.co.uk'
        response = self.login.request(url)

        mock_post.assert_called_once_with(url, data=None, headers=mock_login_headers, cert=mock_cert)
        assert response == mock_create_response
