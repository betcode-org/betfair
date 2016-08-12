import unittest
import mock

from betfairlightweight.streaming.betfairstream import BetfairStream


class BetfairStreamTest(unittest.TestCase):

    def setUp(self):
        self.mock_listener = mock.Mock()
        self.betfair_stream = BetfairStream(1, self.mock_listener, 'app_key', 'session_token', 6, 1024, 'test_stream')

    def test_init(self):
        assert self.betfair_stream.unique_id == 1
        assert self.betfair_stream.listener == self.mock_listener
        assert self.betfair_stream.app_key == 'app_key'
        assert self.betfair_stream.session_token == 'session_token'
        assert self.betfair_stream.timeout == 6
        assert self.betfair_stream.buffer_size == 1024
        assert self.betfair_stream.description == 'test_stream'

        assert self.betfair_stream._socket is None
        assert self.betfair_stream._running is False

    def test_start(self):
        pass

    def test_stop(self):
        pass

    def test_authenticate(self):
        pass

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
