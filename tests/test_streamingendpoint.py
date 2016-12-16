import unittest
from tests import mock

from betfairlightweight import APIClient
from betfairlightweight.endpoints.streaming import Streaming


class StreamingInit(unittest.TestCase):

    def test_base_endpoint_init(self):
        client = APIClient('username', 'password', 'app_key')
        streaming = Streaming(client)
        assert streaming.client == client


class StreamingTest(unittest.TestCase):

    def setUp(self):
        client = APIClient('username', 'password', 'app_key', 'UK')
        self.scores = Streaming(client)

    @mock.patch('betfairlightweight.endpoints.streaming.BetfairStream')
    def test_list_race_details(self, mock_betfair_stream):
        response = self.scores.create_stream(1, 2, 6, 1024, 'TestSocket')

        assert mock_betfair_stream.call_count == 1
        mock_betfair_stream.assert_called_with(1, 2, app_key=self.scores.client.app_key,
                                               session_token=self.scores.client.session_token, timeout=6,
                                               buffer_size=1024, description='TestSocket')
        assert response == mock_betfair_stream()
