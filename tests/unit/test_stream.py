import unittest

from betfairlightweight.streaming.stream import BaseStream, MarketStream, OrderStream
from tests import mock
from tests.unit.tools import create_mock_json


class BaseStreamTest(unittest.TestCase):

    def setUp(self):
        self.listener = mock.Mock()
        self.listener.max_latency = 0.5
        self.stream = BaseStream(self.listener)

    def test_init(self):
        assert self.stream._listener == self.listener

        assert self.stream._initial_clk is None
        assert self.stream._clk is None
        assert self.stream._caches == {}
        assert self.stream._updates_processed == 0
        assert self.stream.time_created is not None
        assert self.stream.time_updated is not None

    @mock.patch('betfairlightweight.streaming.stream.BaseStream._process')
    @mock.patch('betfairlightweight.streaming.stream.BaseStream._update_clk')
    def test_on_subscribe(self, mock_update_clk, mock_process):
        self.stream.on_subscribe({})
        mock_update_clk.assert_called_once_with({})

        self.stream.on_subscribe({'mc': {123}})
        mock_process.assert_called_once_with({123}, None)

    @mock.patch('betfairlightweight.streaming.stream.BaseStream._update_clk')
    def test_on_heartbeat(self, mock_update_clk):
        self.stream.on_heartbeat({})
        mock_update_clk.assert_called_once_with({})

    @mock.patch('betfairlightweight.streaming.stream.BaseStream.on_update')
    def test_on_resubscribe(self, mock_on_update):
        self.stream.on_resubscribe({})
        mock_on_update.assert_called_once_with({})

    @mock.patch('betfairlightweight.streaming.stream.BaseStream._process')
    @mock.patch('betfairlightweight.streaming.stream.BaseStream._calc_latency', return_value=0.1)
    @mock.patch('betfairlightweight.streaming.stream.BaseStream._update_clk')
    def test_on_update(self, mock_update_clk, mock_calc_latency, mock_process):
        mock_response = create_mock_json('tests/resources/streaming_mcm_update.json')
        self.stream.on_update(mock_response.json())

        mock_update_clk.assert_called_with(mock_response.json())
        mock_calc_latency.assert_called_with(mock_response.json().get('pt'))
        mock_process.assert_called_with(mock_response.json().get('mc'), mock_response.json().get('pt'))

        mock_calc_latency.return_value = 10
        self.stream.on_update(mock_response.json())

    def test_clear_cache(self):
        self.stream._caches = {1: 'abc'}
        self.stream.clear_cache()

        assert self.stream._caches == {}

    def test_on_creation(self):
        self.stream._on_creation()

    def test_process(self):
        self.stream._process(None, None)

    def test_on_process(self):
        self.stream.on_process([1, 2])
        self.stream.output_queue.put.assert_called_with([1, 2])

    def test_update_clk(self):
        self.stream._update_clk({'initialClk': 1234})
        assert self.stream._initial_clk == 1234

        self.stream._update_clk({'clk': 123})
        assert self.stream._clk == 123

    def test_unique_id(self):
        assert self.stream.unique_id == self.listener.stream_unique_id

    def test_output_queue(self):
        assert self.stream.output_queue == self.listener.output_queue

    def test_max_latency(self):
        assert self.stream._max_latency == self.listener.max_latency

    def test_lightweight(self):
        assert self.stream._lightweight == self.listener.lightweight

    @mock.patch('time.time', return_value=1485554805.107185)
    def test_calc_latency(self, mock_time):
        pt = 1485554796455
        assert self.stream._calc_latency(pt) is not None
        assert abs(self.stream._calc_latency(pt) - 8.652184) < 1e-5

    def test_len(self):
        assert len(self.stream) == 0

    def test_str(self):
        assert str(self.stream) == 'BaseStream'

    def test_repr(self):
        assert repr(self.stream) == '<BaseStream>'


class MarketStreamTest(unittest.TestCase):

    def setUp(self):
        self.listener = mock.Mock()
        self.stream = MarketStream(self.listener)

    @mock.patch('betfairlightweight.streaming.stream.MarketStream._process')
    @mock.patch('betfairlightweight.streaming.stream.MarketStream._update_clk')
    def test_on_subscribe(self, mock_update_clk, mock_process):
        self.stream.on_subscribe({})
        mock_update_clk.assert_called_once_with({})

        self.stream.on_subscribe({'mc': {123}})
        mock_process.assert_called_once_with({123}, None)

    @mock.patch('betfairlightweight.streaming.stream.MarketBookCache')
    def test_process(self, mock_market_book_cache):
        now = mock.Mock()
        market_books = [mock.Mock()]
        self.stream._caches = mock.Mock()
        # self.stream._process(market_books, now)

    def test_str(self):
        assert str(self.stream) == 'MarketStream'

    def test_repr(self):
        assert repr(self.stream) == '<MarketStream [0]>'


class OrderStreamTest(unittest.TestCase):

    def setUp(self):
        self.listener = mock.Mock()
        self.stream = OrderStream(self.listener)

    def test_process(self):
        pass

    def test_str(self):
        assert str(self.stream) == 'OrderStream'

    def test_repr(self):
        assert repr(self.stream) == '<OrderStream [0]>'
