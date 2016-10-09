import unittest

from betfairlightweight import APIClient
from betfairlightweight.endpoints.inplayservice import InPlayService
from betfairlightweight.exceptions import APIError


class InPlayServiceTest(unittest.TestCase):

    def setUp(self):
        self.client = APIClient('username', 'password', 'app_key', 'UK')
        self.in_play_service = InPlayService(self.client)

    def test_init(self):
        assert self.in_play_service.connect_timeout == 3.05
        assert self.in_play_service.read_timeout == 16
        assert self.in_play_service._error == APIError
        assert self.in_play_service.client == self.client

    def test_url(self):
        assert self.in_play_service.url == 'https://www.betfair.com/inplayservice/v1.1/'

    def test_headers(self):
        assert self.in_play_service.headers == {
            'Connection': 'keep-alive',
            'Content-Type': 'application/json'
        }

    def test_request(self):
        pass

    def test_get_event_timeline(self):
        pass

    def test_get_scores(self):
        pass
