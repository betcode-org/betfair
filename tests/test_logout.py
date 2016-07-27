import unittest
import mock

from tests.tools import create_mock_json
from betfairlightweight.endpoints.logout import Logout
from betfairlightweight import APIClient
from betfairlightweight.exceptions import LogoutError


class LogoutTest(unittest.TestCase):

    def setUp(self):
        client = APIClient('username', 'password', 'app_key', 'UK')
        self.logout = Logout(client)

    def test_call(self):
        pass

    def test_request(self):
        pass

    def test_logout_error_handler(self):
        mock_response = create_mock_json('tests/resources/logout_success.json')
        assert self.logout._error_handler(mock_response.json()) is None

        mock_response = create_mock_json('tests/resources/logout_fail.json')
        with self.assertRaises(LogoutError):
            self.logout._error_handler(mock_response.json())

    def test_url(self):
        assert self.logout.url == 'https://identitysso.betfair.com/api/logout'
