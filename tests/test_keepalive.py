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

    def test_call(self):
        pass

    def test_request(self):
        pass

    def test_keep_alive_error_handler(self):
        mock_response = create_mock_json('tests/resources/keep_alive_success.json')
        assert self.keep_alive._error_handler(mock_response.json()) is None

        mock_response = create_mock_json('tests/resources/keep_alive_fail.json')
        with self.assertRaises(KeepAliveError):
            self.keep_alive._error_handler(mock_response.json())

    def test_url(self):
        assert self.keep_alive.url == 'https://identitysso.betfair.com/api/keepAlive'
