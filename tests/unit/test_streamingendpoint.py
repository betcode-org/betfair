import unittest
from tests import mock

from betfairlightweight import APIClient
from betfairlightweight.endpoints import Streaming


class StreamingTest(unittest.TestCase):

    def setUp(self):
        self.client = APIClient('username', 'password', 'app_key', 'UK')
        self.streaming = Streaming(self.client)

    def test_init(self):
        assert self.streaming.client == self.client

    @mock.patch('betfairlightweight.endpoints.streaming.BetfairStream')
    def test_create_stream(self, mock_betfair_stream):
        response = self.streaming.create_stream(1, 2, 6, 1024, 'TestSocket')

        assert mock_betfair_stream.call_count == 1
        mock_betfair_stream.assert_called_with(1, 2, app_key=self.streaming.client.app_key,
                                               session_token=self.streaming.client.session_token, timeout=6,
                                               buffer_size=1024, description='TestSocket', host=None)
        assert response == mock_betfair_stream()

    @mock.patch('betfairlightweight.endpoints.streaming.HistoricalStream')
    def test_create_historical_stream(self, mock_stream):
        directory = 'test'
        listener = mock.Mock()
        self.streaming.create_historical_stream(directory, listener, 'test')

        listener.register_stream.assert_called_with('HISTORICAL', 'test')
        mock_stream.assert_called_with(directory, listener)
