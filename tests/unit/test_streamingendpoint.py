import unittest
from tests import mock

from betfairlightweight import APIClient
from betfairlightweight.endpoints import Streaming


class StreamingInit(unittest.TestCase):

    def test_base_endpoint_init(self):
        client = APIClient('username', 'password', 'app_key')
        streaming = Streaming(client)
        assert streaming.client == client


class StreamingTest(unittest.TestCase):

    def setUp(self):
        client = APIClient('username', 'password', 'app_key', 'UK')
        self.streaming = Streaming(client)

    @mock.patch('betfairlightweight.endpoints.streaming.BetfairStream')
    def test_list_race_details(self, mock_betfair_stream):
        response = self.streaming.create_stream(1, 2, 6, 1024, 'TestSocket')

        assert mock_betfair_stream.call_count == 1
        mock_betfair_stream.assert_called_with(1, 2, app_key=self.streaming.client.app_key,
                                               session_token=self.streaming.client.session_token, timeout=6,
                                               buffer_size=1024, description='TestSocket', host=None)
        assert response == mock_betfair_stream()

    @mock.patch('betfairlightweight.endpoints.streaming.HistoricalStream')
    def test_create_stream(self, mock_stream):
        dir = 'test'
        listener = mock.Mock()
        self.streaming.create_historical_stream(dir, listener)

        listener.register_stream.assert_called_with('HISTORICAL', 'marketSubscription')
        mock_stream.assert_called_with(dir, listener)
