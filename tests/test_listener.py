import unittest
import mock

from betfairlightweight.streaming.listener import BaseListener, StreamListener


class BaseListenerTest(unittest.TestCase):

    def setUp(self):
        self.base_listener = BaseListener()

    def test_init(self):
        assert self.base_listener.streams == {}

    def test_register_stream(self):
        self.base_listener.register_stream(1, 'heartbeat')

    def test_on_data(self):
        self.base_listener.on_data({}, 2)


class StreamListenerTest(unittest.TestCase):

    def setUp(self):
        self.output_queue = mock.Mock()
        self.stream_listener = StreamListener(self.output_queue)

    def test_init(self):
        assert self.stream_listener.output_queue == self.output_queue

    def test_register_stream(self):
        pass

    def test_on_data(self):
        pass

    def test_on_connection(self):
        self.stream_listener._on_connection({'connectionId': 1234}, 1)
        assert self.stream_listener.connection_id == 1234

    def test_on_status(self):
        self.stream_listener._on_status({}, 1)

    def test_on_change_message(self):
        pass

    def test_add_stream(self):
        pass

    def test_error_handler(self):
        pass
