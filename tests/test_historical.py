import unittest
from tests import mock

from betfairlightweight import APIClient
from betfairlightweight.endpoints.historical import (
    Historical,
    HistoricalStream
)


class HistoricalTest(unittest.TestCase):

    def setUp(self):
        self.client = APIClient('username', 'password', 'app_key', 'UK')
        self.historical = Historical(self.client)

    def test_init(self):
        assert self.historical.client == self.client

    @mock.patch('betfairlightweight.endpoints.historical.HistoricalStream')
    def test_create_stream(self, mock_stream):
        dir = 'test'
        listener = mock.Mock()
        self.historical.create_stream(dir, listener)

        listener.register_stream.assert_called_with('HISTORICAL', 'marketSubscription')
        mock_stream.assert_called_with(dir, listener)


class HistoricalStreamTest(unittest.TestCase):

    def setUp(self):
        self.directory = 'test'
        self.listener = mock.Mock()
        self.stream = HistoricalStream(self.directory, self.listener)

    def test_init(self):
        assert self.stream.directory == self.directory
        assert self.stream.listener == self.listener

    @mock.patch('betfairlightweight.endpoints.historical.HistoricalStream._read_loop')
    def test_start(self, mock_read_loop):
        self.stream.start()
        mock_read_loop.assert_called_with()

    @mock.patch('betfairlightweight.endpoints.historical.HistoricalStream._read_loop')
    @mock.patch('betfairlightweight.endpoints.historical.threading')
    def test_start_thread(self, mock_threading, mock_read_loop):
        self.stream.start(async=True)
        mock_threading.Thread.assert_called_with(name='HistoricalStream', target=mock_read_loop)

    # def test_read_loop(self):
    #     pass
