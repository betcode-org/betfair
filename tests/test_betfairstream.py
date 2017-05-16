import unittest
import socket
import time
import threading
from tests import mock

from betfairlightweight.streaming.betfairstream import BetfairStream
from betfairlightweight.exceptions import SocketError


class BetfairStreamTest(unittest.TestCase):

    def setUp(self):
        self.mock_listener = mock.Mock()
        self.mock_listener.on_data.return_value = False
        self.unique_id = 1
        self.app_key = 'app_key'
        self.session_token = 'session_token'
        self.timeout = 6
        self.buffer_size = 1024
        self.description = 'test_stream'
        self.betfair_stream = BetfairStream(self.unique_id, self.mock_listener, self.app_key, self.session_token,
                                            self.timeout, self.buffer_size, self.description)

    def test_init(self):
        assert self.betfair_stream._unique_id == self.unique_id
        assert self.betfair_stream.listener == self.mock_listener
        assert self.betfair_stream.app_key == self.app_key
        assert self.betfair_stream.session_token == self.session_token
        assert self.betfair_stream.timeout == self.timeout
        assert self.betfair_stream.buffer_size == self.buffer_size
        assert self.betfair_stream.description == self.description
        assert self.betfair_stream.receive_count == 0
        assert self.betfair_stream.datetime_last_received is None

        assert self.betfair_stream._socket is None
        assert self.betfair_stream._running is False

    @mock.patch('betfairlightweight.streaming.betfairstream.BetfairStream.authenticate')
    @mock.patch('betfairlightweight.streaming.betfairstream.BetfairStream._connect')
    @mock.patch('betfairlightweight.streaming.betfairstream.threading')
    @mock.patch('betfairlightweight.streaming.betfairstream.BetfairStream._read_loop')
    def test_start(self, mock_read_loop, mock_threading, mock_connect, mock_authenticate):
        self.betfair_stream._running = True
        self.betfair_stream.start()
        mock_read_loop.assert_called_with()

        self.betfair_stream.start(async=True)
        mock_threading.Thread.assert_called_with(name=self.description, target=mock_read_loop)

        self.betfair_stream._running = False
        self.betfair_stream.start(async=False)
        mock_connect.assert_called_with()
        mock_authenticate.assert_called_with()

    @mock.patch('betfairlightweight.streaming.betfairstream.BetfairStream._create_socket')
    def test_connect(self, mock_create_socket):
        self.betfair_stream._connect()

        assert self.betfair_stream._running is True
        mock_create_socket.assert_called_with()

    def test_stop(self):
        self.betfair_stream.stop()
        assert self.betfair_stream._running is False

    @mock.patch('betfairlightweight.streaming.betfairstream.BetfairStream._send')
    def test_authenticate(self, mock_send):
        self.betfair_stream.authenticate()
        mock_send.assert_called_with(
                {'id': self.betfair_stream._unique_id, 'appKey': self.app_key, 'session': self.session_token, 'op': 'authentication'}
        )

        self.betfair_stream.authenticate()
        mock_send.assert_called_with(
                {'id': self.betfair_stream._unique_id, 'appKey': self.app_key, 'session': self.session_token, 'op': 'authentication'}
        )

    @mock.patch('betfairlightweight.streaming.betfairstream.BetfairStream._send')
    def test_heartbeat(self, mock_send):
        self.betfair_stream.heartbeat()
        mock_send.assert_called_with(
                {'id': self.betfair_stream._unique_id, 'op': 'heartbeat'}
        )

        self.betfair_stream.heartbeat()
        mock_send.assert_called_with(
                {'id': self.betfair_stream._unique_id, 'op': 'heartbeat'}
        )

    @mock.patch('betfairlightweight.streaming.betfairstream.BetfairStream._send')
    def test_subscribe_to_markets(self, mock_send):
        market_filter = {'test': 123}
        market_data_filter = {'another_test': 123}
        initial_clk = 'abcdef'
        clk = 'abc'
        self.betfair_stream.subscribe_to_markets(market_filter, market_data_filter, initial_clk, clk,
                                                 heartbeat_ms=1, conflate_ms=2, segmentation_enabled=False)

        mock_send.assert_called_with(
                {'op': 'marketSubscription', 'marketFilter': market_filter, 'id': self.betfair_stream._unique_id,
                 'marketDataFilter': market_data_filter, 'initialClk': initial_clk, 'clk': clk,
                 'heartbeatMs': 1, 'conflateMs': 2, 'segmentationEnabled': False}
        )
        self.mock_listener.register_stream.assert_called_with(self.betfair_stream._unique_id, 'marketSubscription')

    @mock.patch('betfairlightweight.streaming.betfairstream.BetfairStream._send')
    def test_subscribe_to_orders(self, mock_send):
        initial_clk = 'abcdef'
        clk = 'abc'
        self.betfair_stream.subscribe_to_orders(initial_clk, clk, heartbeat_ms=1, conflate_ms=2,
                                                segmentation_enabled=False)
        mock_send.assert_called_with({
            'orderFilter': 'abcdef', 'id': self.betfair_stream._unique_id, 'op': 'orderSubscription', 'initialClk': 'abc', 'clk': None,
            'heartbeatMs': 1, 'conflateMs': 2, 'segmentationEnabled': False
        })
        self.mock_listener.register_stream.assert_called_with(self.betfair_stream._unique_id, 'orderSubscription')

    @mock.patch('ssl.wrap_socket')
    @mock.patch('socket.socket')
    def test_create_socket(self, mock_socket, mock_wrap_socket):
        self.betfair_stream._create_socket()

        mock_socket.assert_called_with(socket.AF_INET, socket.SOCK_STREAM)
        assert mock_wrap_socket.call_count == 1

    @mock.patch('betfairlightweight.streaming.betfairstream.BetfairStream._data', return_value=False)
    @mock.patch('betfairlightweight.streaming.betfairstream.BetfairStream._receive_all', return_value='{}\r\n')
    def test_read_loop(self, mock_receive_all, mock_data):
        mock_socket = mock.Mock()
        self.betfair_stream._socket = mock_socket

        self.betfair_stream._running = True
        threading.Thread(target=self.betfair_stream._read_loop).start()

        for i in range(0, 2):
            time.sleep(0.1)
        self.betfair_stream._running = False
        time.sleep(0.1)

        mock_data.assert_called_with('{}')
        # mock_socket.close.assert_called_with()
        assert self.betfair_stream.datetime_last_received is not None
        assert self.betfair_stream.receive_count > 0

    @mock.patch('betfairlightweight.streaming.betfairstream.BetfairStream.stop')
    @mock.patch('betfairlightweight.streaming.betfairstream.BetfairStream._receive_all')
    def test_read_loop_error(self, mock_receive_all, mock_stop):
        mock_socket = mock.Mock()
        self.betfair_stream._socket = mock_socket
        self.betfair_stream._running = True

        mock_receive_all.side_effect = socket.error()
        with self.assertRaises(SocketError):
            self.betfair_stream._read_loop()

        mock_receive_all.side_effect = socket.timeout()
        with self.assertRaises(SocketError):
            self.betfair_stream._read_loop()

    def test_receive_all(self):
        mock_socket = mock.Mock()
        data_return_value = b'{"op":"status"}\r\n'
        mock_socket.recv.return_value = data_return_value
        self.betfair_stream._socket = mock_socket

        data = self.betfair_stream._receive_all()
        assert data == ''

        self.betfair_stream._running = True
        data = self.betfair_stream._receive_all()
        mock_socket.recv.assert_called_with(self.buffer_size)
        assert data == data_return_value.decode('utf-8')

    @mock.patch('betfairlightweight.streaming.betfairstream.BetfairStream.stop')
    def test_data(self, mock_stop):
        received_data = {"op": "status"}
        self.betfair_stream._data(received_data)

        self.mock_listener.on_data.assert_called_with(received_data)
        assert mock_stop.called

        self.mock_listener.on_data.return_value = True
        self.betfair_stream._data(received_data)

        self.mock_listener.on_data.assert_called_with(received_data)
        assert mock_stop.call_count == 1

    @mock.patch('betfairlightweight.streaming.betfairstream.BetfairStream.authenticate')
    @mock.patch('betfairlightweight.streaming.betfairstream.BetfairStream._connect')
    def test_send(self, mock_connect, mock_authenticate):
        mock_socket = mock.Mock()
        self.betfair_stream._socket = mock_socket
        message = {'message': 1}

        self.betfair_stream._send(message)
        assert mock_connect.call_count == 1
        assert mock_authenticate.call_count == 1
        assert mock_socket.send.call_count == 1

    def test_repr(self):
        assert repr(self.betfair_stream) == '<BetfairStream>'

    def test_str(self):
        assert str(self.betfair_stream) == '<BetfairStream [not running]>'
        self.betfair_stream._running = True
        assert str(self.betfair_stream) == '<BetfairStream [running]>'
