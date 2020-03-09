import unittest
from unittest import mock
from requests.exceptions import ConnectionError

from betfairlightweight import APIClient
from betfairlightweight.endpoints.login import Login
from betfairlightweight.exceptions import LoginError, APIError, InvalidResponse
from betfairlightweight.resources import LoginResource
from tests.unit.tools import create_mock_json


class LoginTest(unittest.TestCase):
    def setUp(self):
        client = APIClient("username", "password", "app_key", "UK")
        self.login = Login(client)

    @mock.patch("betfairlightweight.endpoints.login.Login.request")
    def test_call(self, mock_response):
        mock_json = create_mock_json("tests/resources/login_success.json")
        mock_response.return_value = (mock.Mock(), mock_json.json(), 1.3)
        response = self.login()

        assert isinstance(response, LoginResource)
        assert self.login.client.session_token == mock_json.json().get("sessionToken")

    @mock.patch("betfairlightweight.baseclient.BaseClient.cert")
    @mock.patch("betfairlightweight.baseclient.BaseClient.login_headers")
    @mock.patch("betfairlightweight.baseclient.requests.post")
    def test_request(self, mock_post, mock_login_headers, mock_cert):
        mock_response = create_mock_json("tests/resources/login_success.json")
        mock_post.return_value = mock_response

        url = "https://identitysso-cert.betfair.com/api/certlogin"
        response = self.login.request()

        mock_post.assert_called_once_with(
            url,
            data={"username": "username", "password": "password"},
            headers=mock_login_headers,
            cert=mock_cert,
        )
        assert response[1] == mock_response.json()

    @mock.patch("betfairlightweight.baseclient.BaseClient.cert")
    @mock.patch("betfairlightweight.baseclient.BaseClient.login_headers")
    @mock.patch("betfairlightweight.baseclient.requests.post")
    def test_request_error(self, mock_post, mock_login_headers, mock_cert):
        mock_post.side_effect = ValueError()

        with self.assertRaises(APIError):
            self.login.request()

        mock_post.side_effect = ConnectionError()
        with self.assertRaises(APIError):
            self.login.request()

    @mock.patch("betfairlightweight.endpoints.login.json.loads", side_effect=ValueError)
    @mock.patch("betfairlightweight.baseclient.BaseClient.cert")
    @mock.patch("betfairlightweight.baseclient.BaseClient.login_headers")
    @mock.patch("betfairlightweight.baseclient.requests.post")
    def test_request_json_error(
        self, mock_post, mock_login_headers, mock_cert, mock_json_loads
    ):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        with self.assertRaises(InvalidResponse):
            self.login.request()

    def test_login_error_handler(self):
        mock_response = create_mock_json("tests/resources/login_success.json")
        assert self.login._error_handler(mock_response.json()) is None

        mock_response = create_mock_json("tests/resources/login_fail.json")
        with self.assertRaises(LoginError):
            self.login._error_handler(mock_response.json())

    def test_url(self):
        assert self.login.url == "https://identitysso-cert.betfair.com/api/certlogin"

    def test_data(self):
        assert self.login.data == {"username": "username", "password": "password"}
