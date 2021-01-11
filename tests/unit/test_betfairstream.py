import unittest
import socket
import time
import threading
from unittest import mock

from betfairlightweight.streaming.betfairstream import (
    BetfairStream,
    HistoricalStream,
    HistoricalGeneratorStream,
)
from betfairlightweight.exceptions import SocketError, ListenerError


class BetfairStreamTest(unittest.TestCase):
    def setUp(self):
        self.mock_listener = mock.Mock()
        self.mock_listener.on_data.return_value = False
        self.unique_id = 1
        self.app_key = "app_key"
        self.session_token = "session_token"
        self.timeout = 6
        self.buffer_size = 1024
        self.betfair_stream = BetfairStream(
            self.unique_id,
            self.mock_listener,
            self.app_key,
            self.session_token,
            self.timeout,
            self.buffer_size,
            None,
        )

    def test_init(self):
        assert self.betfair_stream._unique_id == self.unique_id
        assert self.betfair_stream.listener == self.mock_listener
        assert self.betfair_stream.app_key == self.app_key
        assert self.betfair_stream.session_token == self.session_token
        assert self.betfair_stream.timeout == self.timeout
        assert self.betfair_stream.buffer_size == self.buffer_size
        assert self.betfair_stream.host == "stream-api.betfair.com"
        assert self.betfair_stream.receive_count == 0
        assert self.betfair_stream.datetime_last_received is None

        assert self.betfair_stream._socket is None
        assert self.betfair_stream._running is False

    def test_host_init(self):
        betfair_stream = BetfairStream(
            self.unique_id,
            self.mock_listener,
            self.app_key,
            self.session_token,
            self.timeout,
            self.buffer_size,
            "integration",
        )
        assert betfair_stream.host == "stream-api-integration.betfair.com"

    @mock.patch("betfairlightweight.streaming.betfairstream.BetfairStream.authenticate")
    @mock.patch("betfairlightweight.streaming.betfairstream.BetfairStream._connect")
    @mock.patch("betfairlightweight.streaming.betfairstream.BetfairStream._read_loop")
    def test_start(self, mock_read_loop, mock_connect, mock_authenticate):
        self.betfair_stream._running = True
        self.betfair_stream.start()
        mock_read_loop.assert_called_with()

        self.betfair_stream._running = False
        self.betfair_stream.start()
        mock_connect.assert_called_with()
        mock_authenticate.assert_called_with()

    @mock.patch(
        "betfairlightweight.streaming.betfairstream.BetfairStream._create_socket"
    )
    def test_connect(self, mock_create_socket):
        self.betfair_stream._connect()

        assert self.betfair_stream._running is True
        mock_create_socket.assert_called_with()

    def test_stop(self):
        self.betfair_stream.stop()
        assert self.betfair_stream._running is False
        assert self.betfair_stream._socket is None

    @mock.patch("betfairlightweight.streaming.betfairstream.BetfairStream._send")
    def test_authenticate(self, mock_send):
        self.betfair_stream.authenticate()
        mock_send.assert_called_with(
            {
                "id": self.betfair_stream._unique_id,
                "appKey": self.app_key,
                "session": self.session_token,
                "op": "authentication",
            }
        )

        self.betfair_stream.authenticate()
        mock_send.assert_called_with(
            {
                "id": self.betfair_stream._unique_id,
                "appKey": self.app_key,
                "session": self.session_token,
                "op": "authentication",
            }
        )

    @mock.patch("betfairlightweight.streaming.betfairstream.BetfairStream._send")
    def test_heartbeat(self, mock_send):
        self.betfair_stream.heartbeat()
        mock_send.assert_called_with(
            {"id": self.betfair_stream._unique_id, "op": "heartbeat"}
        )

        self.betfair_stream.heartbeat()
        mock_send.assert_called_with(
            {"id": self.betfair_stream._unique_id, "op": "heartbeat"}
        )

    @mock.patch("betfairlightweight.streaming.betfairstream.BetfairStream._send")
    def test_subscribe_to_markets(self, mock_send):
        market_filter = {"test": 123}
        market_data_filter = {"another_test": 123}
        self.betfair_stream.subscribe_to_markets(
            market_filter,
            market_data_filter,
            heartbeat_ms=1,
            conflate_ms=2,
            segmentation_enabled=False,
        )

        mock_send.assert_called_with(
            {
                "op": "marketSubscription",
                "marketFilter": market_filter,
                "id": self.betfair_stream._unique_id,
                "marketDataFilter": market_data_filter,
                "initialClk": None,
                "clk": None,
                "heartbeatMs": 1,
                "conflateMs": 2,
                "segmentationEnabled": False,
            }
        )
        self.mock_listener.register_stream.assert_called_with(
            self.betfair_stream._unique_id, "marketSubscription"
        )

    @mock.patch("betfairlightweight.streaming.betfairstream.BetfairStream._send")
    def test_resubscribe_to_markets(self, mock_send):
        market_filter = {"test": 123}
        market_data_filter = {"another_test": 123}
        initial_clk = "abcdef"
        clk = "abc"
        self.betfair_stream.subscribe_to_markets(
            market_filter,
            market_data_filter,
            initial_clk,
            clk,
            heartbeat_ms=1,
            conflate_ms=2,
            segmentation_enabled=False,
        )

        mock_send.assert_called_with(
            {
                "op": "marketSubscription",
                "marketFilter": market_filter,
                "id": self.betfair_stream._unique_id,
                "marketDataFilter": market_data_filter,
                "initialClk": initial_clk,
                "clk": clk,
                "heartbeatMs": 1,
                "conflateMs": 2,
                "segmentationEnabled": False,
            }
        )
        assert not self.mock_listener.register_stream.called
        self.mock_listener.update_unique_id.assert_called_with(
            self.betfair_stream._unique_id
        )

    @mock.patch("betfairlightweight.streaming.betfairstream.BetfairStream._send")
    def test_subscribe_to_orders(self, mock_send):
        order_filter = {"test": 123}
        self.betfair_stream.subscribe_to_orders(
            order_filter, heartbeat_ms=1, conflate_ms=2, segmentation_enabled=False
        )
        mock_send.assert_called_with(
            {
                "orderFilter": order_filter,
                "id": self.betfair_stream._unique_id,
                "op": "orderSubscription",
                "initialClk": None,
                "clk": None,
                "heartbeatMs": 1,
                "conflateMs": 2,
                "segmentationEnabled": False,
            }
        )
        self.mock_listener.register_stream.assert_called_with(
            self.betfair_stream._unique_id, "orderSubscription"
        )

    @mock.patch("betfairlightweight.streaming.betfairstream.BetfairStream._send")
    def test_subscribe_to_orders_resubscribe(self, mock_send):
        order_filter = {"test": 123}
        initial_clk = "abcdef"
        clk = "abc"
        self.betfair_stream.subscribe_to_orders(
            order_filter,
            initial_clk,
            clk,
            heartbeat_ms=1,
            conflate_ms=2,
            segmentation_enabled=False,
        )
        mock_send.assert_called_with(
            {
                "orderFilter": order_filter,
                "id": self.betfair_stream._unique_id,
                "op": "orderSubscription",
                "initialClk": initial_clk,
                "clk": clk,
                "heartbeatMs": 1,
                "conflateMs": 2,
                "segmentationEnabled": False,
            }
        )
        assert not self.mock_listener.register_stream.called
        self.mock_listener.update_unique_id.assert_called_with(
            self.betfair_stream._unique_id
        )

    @mock.patch("betfairlightweight.streaming.betfairstream.BetfairStream._send")
    def test_subscribe_to_races(self, mock_send):
        self.betfair_stream.subscribe_to_races()

        mock_send.assert_called_with(
            {"op": "raceSubscription", "id": self.betfair_stream._unique_id}
        )
        assert not self.mock_listener.register_stream.assert_called_with(
            self.betfair_stream._unique_id, "raceSubscription"
        )

    @mock.patch("ssl.wrap_socket")
    @mock.patch("socket.socket")
    def test_create_socket(self, mock_socket, mock_wrap_socket):
        self.betfair_stream._create_socket()

        mock_socket.assert_called_with(socket.AF_INET, socket.SOCK_STREAM)
        assert mock_wrap_socket.call_count == 1

    @mock.patch(
        "betfairlightweight.streaming.betfairstream.BetfairStream._data",
        return_value=False,
    )
    @mock.patch(
        "betfairlightweight.streaming.betfairstream.BetfairStream._receive_all",
        return_value="{}\r\n",
    )
    def test_read_loop(self, mock_receive_all, mock_data):
        mock_socket = mock.Mock()
        self.betfair_stream._socket = mock_socket

        self.betfair_stream._running = True
        threading.Thread(target=self.betfair_stream._read_loop).start()

        for i in range(0, 2):
            time.sleep(0.1)
        self.betfair_stream._running = False
        time.sleep(0.1)

        mock_data.assert_called_with("{}")
        mock_receive_all.assert_called_with()
        assert self.betfair_stream.datetime_last_received is not None
        assert self.betfair_stream.receive_count > 0

    def test_receive_all(self):
        mock_socket = mock.Mock()
        data_return_value = b'{"op":"status"}\r\n'
        mock_socket.recv.return_value = data_return_value
        self.betfair_stream._socket = mock_socket

        data = self.betfair_stream._receive_all()
        assert data == ""

        self.betfair_stream._running = True
        data = self.betfair_stream._receive_all()
        mock_socket.recv.assert_called_with(self.buffer_size)
        assert data == data_return_value.decode("utf-8")

    @mock.patch("betfairlightweight.streaming.betfairstream.BetfairStream.stop")
    def test_receive_all_closed(self, mock_stop):
        mock_socket = mock.Mock()
        data_return_value = b""
        mock_socket.recv.return_value = data_return_value
        self.betfair_stream._socket = mock_socket
        self.betfair_stream._running = True

        with self.assertRaises(SocketError):
            self.betfair_stream._receive_all()
        mock_stop.assert_called_with()

    @mock.patch("betfairlightweight.streaming.betfairstream.BetfairStream.stop")
    def test_receive_all_error(self, mock_stop):
        mock_socket = mock.Mock()
        self.betfair_stream._socket = mock_socket

        self.betfair_stream._running = True
        mock_socket.recv.side_effect = socket.error()
        with self.assertRaises(SocketError):
            self.betfair_stream._receive_all()
        mock_stop.assert_called_with()

    @mock.patch("betfairlightweight.streaming.betfairstream.BetfairStream.stop")
    def test_receive_all_timeout(self, mock_stop):
        mock_socket = mock.Mock()
        self.betfair_stream._socket = mock_socket

        self.betfair_stream._running = True
        mock_socket.recv.side_effect = socket.timeout()
        with self.assertRaises(SocketError):
            self.betfair_stream._receive_all()
        mock_stop.assert_called_with()

    @mock.patch("betfairlightweight.streaming.betfairstream.BetfairStream.stop")
    def test_data(self, mock_stop):
        received_data = {"op": "status"}
        with self.assertRaises(ListenerError):
            self.betfair_stream._data(received_data)

        self.mock_listener.on_data.assert_called_with(received_data)
        assert mock_stop.called

        self.mock_listener.on_data.return_value = True
        self.betfair_stream._data(received_data)

        self.mock_listener.on_data.assert_called_with(received_data)
        assert mock_stop.call_count == 1

    @mock.patch("betfairlightweight.streaming.betfairstream.BetfairStream.authenticate")
    @mock.patch("betfairlightweight.streaming.betfairstream.BetfairStream._connect")
    def test_send(self, mock_connect, mock_authenticate):
        mock_socket = mock.Mock()
        self.betfair_stream._socket = mock_socket
        message = {"message": 1}

        self.betfair_stream._send(message)
        assert mock_connect.call_count == 1
        assert mock_authenticate.call_count == 1
        assert mock_socket.sendall.call_count == 1
        try:
            import orjson

            rust = True
        except:
            rust = False
        if rust:
            mock_socket.sendall.assert_called_with(b'{"message":1}\r\n')
        else:
            mock_socket.sendall.assert_called_with(b'{"message": 1}\r\n')

    @mock.patch("betfairlightweight.streaming.betfairstream.BetfairStream.stop")
    def test_send_timeout(self, mock_stop):
        self.betfair_stream._running = True
        mock_socket = mock.Mock()
        self.betfair_stream._socket = mock_socket
        mock_socket.sendall.side_effect = socket.timeout()
        message = {"message": 1}

        with self.assertRaises(SocketError):
            self.betfair_stream._send(message)
        mock_stop.assert_called_with()

    @mock.patch("betfairlightweight.streaming.betfairstream.BetfairStream.stop")
    def test_send_error(self, mock_stop):
        self.betfair_stream._running = True
        mock_socket = mock.Mock()
        self.betfair_stream._socket = mock_socket
        mock_socket.sendall.side_effect = socket.error()
        message = {"message": 1}

        with self.assertRaises(SocketError):
            self.betfair_stream._send(message)
        mock_stop.assert_called_with()

    def test_repr(self):
        assert repr(self.betfair_stream) == "<BetfairStream>"

    def test_str(self):
        assert str(self.betfair_stream) == "<BetfairStream [not running]>"
        self.betfair_stream._running = True
        assert str(self.betfair_stream) == "<BetfairStream [running]>"


class HistoricalStreamTest(unittest.TestCase):
    def setUp(self):
        self.file_path = "tests/resources/historicaldata/BASIC-1.132153978"
        self.listener = mock.Mock()
        self.operation = "marketSubscription"
        self.stream = HistoricalStream(self.file_path, self.listener, self.operation, 0)

    def test_init(self):
        assert self.stream.file_path == self.file_path
        assert self.stream.listener == self.listener
        assert self.stream._running is False
        assert self.stream.operation == self.operation

    @mock.patch("betfairlightweight.endpoints.streaming.HistoricalStream._read_loop")
    def test_start(self, mock_read_loop):
        self.stream.start()
        mock_read_loop.assert_called_with()
        assert self.stream._running is True

    def test_stop(self):
        self.stream._running = True
        self.stream.stop()
        assert self.stream._running is False

    @mock.patch("betfairlightweight.streaming.betfairstream.HistoricalStream.stop")
    def test__read_loop(self, mock_stop):
        self.stream._running = True
        self.stream._read_loop()
        self.assertEqual(self.listener.on_data.call_count, 480)
        self.listener.on_data.snap()
        mock_stop.assert_called_with()
        self.assertTrue(self.stream._running)
        self.listener.register_stream.assert_called_with(0, self.operation)


class HistoricalGeneratorStreamTest(unittest.TestCase):
    def setUp(self):
        self.file_path = "tests/resources/historicaldata/BASIC-1.132153978"
        self.listener = mock.Mock()
        self.operation = "marketSubscription"
        self.stream = HistoricalGeneratorStream(
            self.file_path, self.listener, self.operation, 0
        )

    def test_init(self):
        assert self.stream.file_path == self.file_path
        assert self.stream.listener == self.listener
        assert self.stream._running is False
        assert self.stream.operation == self.operation

    @mock.patch(
        "betfairlightweight.streaming.betfairstream.HistoricalGeneratorStream._read_loop"
    )
    def test_get_generator(self, mock_read_loop):
        self.assertEqual(self.stream.get_generator(), mock_read_loop)

    @mock.patch(
        "betfairlightweight.streaming.betfairstream.HistoricalGeneratorStream.stop"
    )
    def test__read_loop(self, mock_stop):
        data = [i for i in self.stream._read_loop()]
        self.assertEqual(len(data), 480)
        self.assertEqual(self.listener.on_data.call_count, 480)
        self.listener.on_data.snap()
        mock_stop.assert_called_with()
        self.assertTrue(self.stream._running)
        self.listener.register_stream.assert_called_with(0, self.operation)
