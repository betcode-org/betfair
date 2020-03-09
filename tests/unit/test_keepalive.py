import unittest
from unittest import mock
from requests.exceptions import ConnectionError

from betfairlightweight import APIClient
from betfairlightweight.endpoints.keepalive import KeepAlive, APIError
from betfairlightweight.exceptions import KeepAliveError, InvalidResponse
from betfairlightweight.resources.authresources import KeepAliveResource
from tests.unit.tools import create_mock_json


class KeepAliveTest(unittest.TestCase):
    def setUp(self):
        client = APIClient("username", "password", "app_key", "UK")
        self.keep_alive = KeepAlive(client)

    @mock.patch("betfairlightweight.endpoints.keepalive.KeepAlive.request")
    def test_call(self, mock_response):
        mock = create_mock_json("tests/resources/keep_alive_success.json")
        mock_response.return_value = (mock.Mock(), mock.json(), 1.3)
        response = self.keep_alive()

        assert isinstance(response, KeepAliveResource)
        assert self.keep_alive.client.session_token == mock.json().get("token")

    @mock.patch("betfairlightweight.baseclient.BaseClient.keep_alive_headers")
    @mock.patch("betfairlightweight.baseclient.requests.post")
    def test_request(self, mock_post, mock_keep_alive_headers):
        mock_response = create_mock_json("tests/resources/logout_success.json")
        mock_post.return_value = mock_response

        url = "https://identitysso.betfair.com/api/keepAlive"
        response = self.keep_alive.request()

        mock_post.assert_called_once_with(url, headers=mock_keep_alive_headers)
        assert response[1] == mock_response.json()

    @mock.patch("betfairlightweight.baseclient.BaseClient.keep_alive_headers")
    @mock.patch("betfairlightweight.baseclient.requests.post")
    def test_request_error(self, mock_post, mock_keep_alive_headers):
        mock_post.side_effect = ValueError()

        with self.assertRaises(APIError):
            self.keep_alive.request()

        mock_post.side_effect = ConnectionError()

        with self.assertRaises(APIError):
            self.keep_alive.request()

    @mock.patch(
        "betfairlightweight.endpoints.keepalive.json.loads", side_effect=ValueError
    )
    @mock.patch("betfairlightweight.baseclient.BaseClient.keep_alive_headers")
    @mock.patch("betfairlightweight.baseclient.requests.post")
    def test_request_json_error(
        self, mock_post, mock_keep_alive_headers, mock_json_loads
    ):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        with self.assertRaises(InvalidResponse):
            self.keep_alive.request()

    def test_keep_alive_error_handler(self):
        mock_response = create_mock_json("tests/resources/keep_alive_success.json")
        assert self.keep_alive._error_handler(mock_response.json()) is None

        mock_response = create_mock_json("tests/resources/keep_alive_fail.json")
        with self.assertRaises(KeepAliveError):
            self.keep_alive._error_handler(mock_response.json())

    def test_url(self):
        assert self.keep_alive.url == "https://identitysso.betfair.com/api/keepAlive"
