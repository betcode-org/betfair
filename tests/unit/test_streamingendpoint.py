import unittest
from unittest import mock

from betfairlightweight import APIClient
from betfairlightweight.endpoints import Streaming


class StreamingTest(unittest.TestCase):
    def setUp(self):
        self.client = APIClient("username", "password", "app_key", "UK")
        self.streaming = Streaming(self.client)

    def test_init(self):
        self.assertEqual(self.streaming.client, self.client)

    @mock.patch("betfairlightweight.endpoints.streaming.BetfairStream")
    def test_create_stream(self, mock_betfair_stream):
        response = self.streaming.create_stream(1, 2, 6, 1024)

        assert mock_betfair_stream.call_count == 1
        mock_betfair_stream.assert_called_with(
            1,
            2,
            app_key=self.streaming.client.app_key,
            session_token=self.streaming.client.session_token,
            timeout=6,
            buffer_size=1024,
            host=None,
        )
        assert response == mock_betfair_stream()

    @mock.patch("betfairlightweight.endpoints.streaming.HistoricalStream")
    def test_create_historical_stream(self, mock_stream):
        file_path = "test"
        listener = mock.Mock()
        self.streaming.create_historical_stream(file_path=file_path, listener=listener)

        listener.register_stream.assert_called_with(0, "marketSubscription")
        mock_stream.assert_called_with(file_path, listener)

    @mock.patch("betfairlightweight.endpoints.streaming.HistoricalGeneratorStream")
    def test_create_historical_generator_stream(self, mock_stream):
        file_path = "test"
        listener = mock.Mock()
        self.streaming.create_historical_generator_stream(
            file_path=file_path, listener=listener
        )

        listener.register_stream.assert_called_with(0, "marketSubscription")
        mock_stream.assert_called_with(file_path, listener)

    @mock.patch("betfairlightweight.endpoints.streaming.HistoricalStream")
    def test_create_historical_stream_with_directory(self, mock_stream):
        file_path = "test"
        listener = mock.Mock()

        with self.assertWarns(DeprecationWarning):
            self.streaming.create_historical_stream(
                directory=file_path, listener=listener
            )

            listener.register_stream.assert_called_with(0, "marketSubscription")
            mock_stream.assert_called_with(file_path, listener)

    @mock.patch("betfairlightweight.endpoints.streaming.HistoricalGeneratorStream")
    def test_create_historical_generator_stream_with_directory(self, mock_stream):
        file_path = "test"
        listener = mock.Mock()

        with self.assertWarns(DeprecationWarning):
            self.streaming.create_historical_generator_stream(
                directory=file_path, listener=listener
            )

            listener.register_stream.assert_called_with(0, "marketSubscription")
            mock_stream.assert_called_with(file_path, listener)
