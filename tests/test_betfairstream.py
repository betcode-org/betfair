import unittest
from unittest import mock

from betfairlightweight.streaming.betfairstream import BetfairStream


class BetfairStreamTest(unittest.TestCase):

    def setUp(self):
        self.mock_listener = mock.Mock()
        self.unique_id = 1
        self.app_key = 'app_key'
        self.session_token = 'session_token'
        self.timeout = 6
        self.buffer_size = 1024
        self.description = 'test_stream'
        self.betfair_stream = BetfairStream(self.unique_id, self.mock_listener, self.app_key, self.session_token,
                                            self.timeout, self.buffer_size, self.description)

    def test_init(self):
        assert self.betfair_stream.unique_id == self.unique_id
        assert self.betfair_stream.listener == self.mock_listener
        assert self.betfair_stream.app_key == self.app_key
        assert self.betfair_stream.session_token == self.session_token
        assert self.betfair_stream.timeout == self.timeout
        assert self.betfair_stream.buffer_size == self.buffer_size
        assert self.betfair_stream.description == self.description

        assert self.betfair_stream._socket is None
        assert self.betfair_stream._running is False

    @mock.patch('betfairlightweight.streaming.betfairstream.BetfairStream._read_loop')
    @mock.patch('betfairlightweight.streaming.betfairstream.BetfairStream._receive_all', return_value={})
    @mock.patch('betfairlightweight.streaming.betfairstream.BetfairStream._create_socket')
    def test_start(self, mock_create_socket, mock_receive_all, mock_read_loop):
        self.betfair_stream.start()

        assert self.betfair_stream._running is True
        mock_create_socket.assert_called_with()
        mock_receive_all.assert_called_with()
        self.mock_listener.on_data.assert_called_with({}, self.unique_id)
        mock_read_loop.assert_called_with()

    def test_stop(self):
        self.betfair_stream.stop()
        assert self.betfair_stream._running is False

    @mock.patch('betfairlightweight.streaming.betfairstream.BetfairStream._send')
    def test_authenticate(self, mock_send):
        self.betfair_stream.authenticate()
        mock_send.assert_called_with(
                {'id': self.unique_id, 'appKey': self.app_key, 'session': self.session_token, 'op': 'authentication'}
        )

        self.betfair_stream.authenticate(999)
        mock_send.assert_called_with(
                {'id': 999, 'appKey': self.app_key, 'session': self.session_token, 'op': 'authentication'}
        )

    def test_heartbeat(self):
        pass

    def test_subscribe_to_markets(self):
        pass

    def test_subscribe_to_orders(self):
        pass

    def test_create_socket(self):
        pass

    def test_read_loop(self):
        pass

    def test_receive_all(self):
        pass

    def test_data(self):
        pass

    def test_send(self):
        pass
