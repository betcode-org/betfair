import unittest
from unittest import mock
from requests.exceptions import ConnectionError

from betfairlightweight import APIClient
from betfairlightweight.endpoints.logout import Logout
from betfairlightweight.exceptions import LogoutError, APIError, InvalidResponse
from betfairlightweight.resources import LogoutResource
from tests.unit.tools import create_mock_json


class LogoutTest(unittest.TestCase):
    def setUp(self):
        client = APIClient("username", "password", "app_key", "UK")
        self.logout = Logout(client)

    @mock.patch("betfairlightweight.endpoints.logout.Logout.request")
    def test_call(self, mock_response):
        mock = create_mock_json("tests/resources/logout_success.json")
        mock_response.return_value = (mock.Mock(), mock.json(), 1.3)
        response = self.logout()

        assert isinstance(response, LogoutResource)
        assert self.logout.client.session_token is None

    @mock.patch("betfairlightweight.baseclient.BaseClient.keep_alive_headers")
    @mock.patch("betfairlightweight.baseclient.requests.post")
    def test_request(self, mock_post, mock_logout_headers):
        mock_response = create_mock_json("tests/resources/logout_success.json")
        mock_post.return_value = mock_response

        url = "https://identitysso.betfair.com/api/logout"
        response = self.logout.request()

        mock_post.assert_called_once_with(url, headers=mock_logout_headers)
        assert response[1] == mock_response.json()

    @mock.patch("betfairlightweight.baseclient.BaseClient.cert")
    @mock.patch("betfairlightweight.baseclient.BaseClient.keep_alive_headers")
    @mock.patch("betfairlightweight.baseclient.requests.post")
    def test_request_error(self, mock_post, mock_logout_headers, mock_cert):
        mock_post.side_effect = ValueError()

        with self.assertRaises(APIError):
            self.logout.request()

        mock_post.side_effect = ConnectionError()
        with self.assertRaises(APIError):
            self.logout.request()

    @mock.patch(
        "betfairlightweight.endpoints.logout.json.loads", side_effect=ValueError
    )
    @mock.patch("betfairlightweight.baseclient.BaseClient.cert")
    @mock.patch("betfairlightweight.baseclient.BaseClient.keep_alive_headers")
    @mock.patch("betfairlightweight.baseclient.requests.post")
    def test_request_json_error(
        self, mock_post, mock_logout_headers, mock_cert, mock_json_loads
    ):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        with self.assertRaises(InvalidResponse):
            self.logout.request()

    def test_logout_error_handler(self):
        mock_response = create_mock_json("tests/resources/logout_success.json")
        assert self.logout._error_handler(mock_response.json()) is None

        mock_response = create_mock_json("tests/resources/logout_fail.json")
        with self.assertRaises(LogoutError):
            self.logout._error_handler(mock_response.json())

    def test_url(self):
        assert self.logout.url == "https://identitysso.betfair.com/api/logout"
