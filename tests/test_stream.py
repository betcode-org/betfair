import unittest
import mock

from betfairlightweight.streaming.stream import Stream


class BetfairStreamTest(unittest.TestCase):

    def setUp(self):
        self.output_queue = mock.Mock()
        self.stream = Stream(1, 'market', self.output_queue)

    def test_init(self):
        assert self.stream.unique_id == 1
        assert self.stream.stream_type == 'market'
        assert self.stream.output_queue == self.output_queue

        assert self.stream._initial_clk is None
        assert self.stream._clk is None
        assert self.stream._caches == {}
        assert self.stream._updates_processed == 0
        assert self.stream.time_created is not None
        assert self.stream.time_updated is not None

    @mock.patch('betfairlightweight.streaming.stream.Stream._update_clk')
    def test_on_heartbeat(self, mock_update_clk):
        self.stream.on_heartbeat({})
        mock_update_clk.assert_called_once_with({})

    @mock.patch('betfairlightweight.streaming.stream.Stream._update_clk')
    def test_on_resubscribe(self, mock_update_clk):
        self.stream.on_resubscribe({})
        mock_update_clk.assert_called_once_with({})

    @mock.patch('betfairlightweight.streaming.stream.Stream._process_order_books')
    @mock.patch('betfairlightweight.streaming.stream.Stream._process_market_books')
    @mock.patch('betfairlightweight.streaming.stream.Stream._update_clk')
    def test_on_subscribe(self, mock_update_clk, mock_process_market_books, mock_process_order_books):
        self.stream.on_subscribe({}, 'test')
        mock_update_clk.assert_called_once_with({})

        self.stream.on_subscribe({'mc': {123}}, 'mcm')
        mock_process_market_books.assert_called_once_with({123}, None)

        self.stream.on_subscribe({'oc': {123}}, 'ocm')
        mock_process_order_books.assert_called_once_with({123}, None)

    def test_on_update(self):
        pass

    def test_process_market_books(self):
        pass

    def test_process_order_books(self):
        pass

    def test_on_creation(self):
        self.stream._on_creation()

    def test_update_clk(self):
        self.stream._update_clk({'initialClk': 1234})
        assert self.stream._initial_clk == 1234

        self.stream._update_clk({'clk': 123})
        assert self.stream._clk == 123

    def test_calc_latency(self):
        assert self.stream._calc_latency(1234) is not None
