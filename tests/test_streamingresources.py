import unittest
from unittest import mock

from betfairlightweight.resources.streamingresources import (
    MarketDefinition, OrderBookCache, OrderBookRunner, Matched, UnmatchedOrder, MarketBookCache, RunnerBook
)
from tests.tools import create_mock_json


class TestMarketDefinition(unittest.TestCase):

    def setUp(self):
        self.mock_response = create_mock_json('tests/resources/streaming_market_definition.json')
        self.market_definition = MarketDefinition(**self.mock_response.json())

    def test_init(self):
        assert self.market_definition._data == self.mock_response.json()
        assert len(self.market_definition.runners) == 7
        assert self.market_definition.bsp_market is True
        assert self.market_definition.market_base_rate == 5


class TestOrderBookCache(unittest.TestCase):

    def setUp(self):
        self.order_book_cache = OrderBookCache(**{})
        self.runner = mock.Mock()
        self.runner.selection_id = 10895629
        self.runner.serialise_orders = []
        self.order_book_cache.runners = [self.runner]

    def test_update_cache(self):
        mock_response = create_mock_json('tests/resources/streaming_ocm_UPDATE.json')
        for order_book in mock_response.json().get('oc'):
            self.order_book_cache.update_cache(order_book)

            for order_changes in order_book.get('orc'):
                self.runner.update_matched_lays.assert_called_with(order_changes.get('ml', []))
                self.runner.update_matched_backs.assert_called_with(order_book.get('mb', []))
                self.runner.update_unmatched.assert_called_with(order_changes.get('uo', []))

    @mock.patch('betfairlightweight.resources.streamingresources.OrderBookRunner')
    def test_update_cache_new(self, mock_order_book_runner):
        self.runner.selection_id = 108956
        mock_response = create_mock_json('tests/resources/streaming_ocm_UPDATE.json')
        for order_book in mock_response.json().get('oc'):
            self.order_book_cache.update_cache(order_book)

            for order_changes in order_book.get('orc'):
                mock_order_book_runner.assert_called_with(**order_changes)

    @mock.patch('betfairlightweight.resources.streamingresources.OrderBookCache.serialise')
    @mock.patch('betfairlightweight.resources.streamingresources.CurrentOrders')
    def test_create_order_book(self, mock_current_orders, mock_serialise):
        current_orders = self.order_book_cache.create_order_book

        mock_current_orders.assert_called_with(**mock_serialise)
        assert current_orders == mock_current_orders()

    def test_serialise(self):
        serialised = self.order_book_cache.serialise

        assert serialised == {'currentOrders': [], 'moreAvailable': False}


class TestOrderBookRunner(unittest.TestCase):

    def setUp(self):
        self.order_book_runner = OrderBookRunner(**{})

    @mock.patch('betfairlightweight.resources.streamingresources.Matched')
    def test_update_matched_fresh(self, mock_matched):
        matched_lays = [[1.01, 4.00]]

        self.order_book_runner.update_matched_lays(matched_lays)
        assert len(self.order_book_runner.matched_lays) == 1
        assert self.order_book_runner.matched_lays[0] == mock_matched()

    @mock.patch('betfairlightweight.resources.streamingresources.Matched')
    def test_update_matched_lays_new(self, mock_matched):
        mock_matched_lay = mock.Mock()
        mock_matched_lay.price = 1.01
        mock_matched_lay.size = 2.00
        self.order_book_runner.matched_lays = [mock_matched_lay]

        matched_lays = [[1.03, 2.00]]
        self.order_book_runner.update_matched_lays(matched_lays)

        assert len(self.order_book_runner.matched_lays) == 2

    @mock.patch('betfairlightweight.resources.streamingresources.Matched')
    def test_update_matched_lays(self, mock_matched):
        mock_matched_lay = mock.Mock()
        mock_matched_lay.price = 1.01
        mock_matched_lay.size = 2.00
        self.order_book_runner.matched_lays = [mock_matched_lay]

        matched_lays = [[1.01, 4.00]]
        self.order_book_runner.update_matched_lays(matched_lays)

        assert len(self.order_book_runner.matched_lays) == 1
        assert mock_matched_lay.size == 4.00
        assert mock_matched_lay.price == 1.01


class TestMatched(unittest.TestCase):

    def setUp(self):
        self.price = 1.01
        self.size = 2.00
        self.matched = Matched(self.price, self.size)

    def test_init(self):
        assert self.matched.price == self.price
        assert self.matched.size == self.size


class TestUnmatchedOrder(unittest.TestCase):

    def setUp(self):
        self.unmatched_order = UnmatchedOrder(**{})

    # def test_serialise(self):
    #     self.unmatched_order.serialise('1.23', 12345)


class TestMarketBookCache(unittest.TestCase):

    def setUp(self):
        self.market_book_cache = MarketBookCache(**{})

    @mock.patch('betfairlightweight.resources.streamingresources.MarketDefinition')
    @mock.patch('betfairlightweight.resources.streamingresources.MarketBookCache.strip_datetime')
    def test_update_cache_md(self, mock_strip_datetime, mock_market_definition):
        publish_time = mock.Mock()
        market_change = create_mock_json('tests/resources/streaming_mcm_UPDATE_md.json')
        book_data = market_change.json().get('mc')

        for book in book_data:
            self.market_book_cache.update_cache(book, publish_time)
            mock_strip_datetime.assert_called_with(publish_time)
            mock_market_definition.assert_called_with(**book.get('marketDefinition'))

    @mock.patch('betfairlightweight.resources.streamingresources.MarketBookCache.strip_datetime')
    def test_update_cache_md(self, mock_strip_datetime):
        publish_time = mock.Mock()
        market_change = create_mock_json('tests/resources/streaming_mcm_UPDATE_tv.json')
        book_data = market_change.json().get('mc')

        for book in book_data:
            self.market_book_cache.update_cache(book, publish_time)
            mock_strip_datetime.assert_called_with(publish_time)
            assert self.market_book_cache.total_matched == book.get('tv')

    # @mock.patch('betfairlightweight.resources.streamingresources.MarketBookCache.strip_datetime')
    # def test_update_cache_rc(self, mock_strip_datetime):
    #     publish_time = mock.Mock()
    #     market_change = create_mock_json('tests/resources/streaming_mcm_UPDATE.json')
    #     book_data = market_change.json().get('mc')
    #
    #     for book in book_data:
    #         self.market_book_cache.update_cache(book, publish_time)
    #         mock_strip_datetime.assert_called_with(publish_time)
    #
    #         assert self.market_book_cache.total_matched == book.get('tv')

    @mock.patch('betfairlightweight.resources.streamingresources.MarketBookCache.serialise')
    @mock.patch('betfairlightweight.resources.streamingresources.MarketBook')
    def test_create_market_book(self, mock_market_book, mock_serialise):
        market_book = self.market_book_cache.create_market_book()

        assert market_book == mock_market_book()()
        mock_market_book.assert_called_with()


class TestRunnerBook(unittest.TestCase):

    def setUp(self):
        self.runner_book = RunnerBook(**{})

    def test_traded_update_new(self):
        traded_update = [[18.5, 1.2]]

        self.runner_book.update_traded(traded_update)
        assert self.runner_book.traded == traded_update

    def test_traded_update_removal(self):
        traded_update = None
        self.runner_book.traded = [[18.5, 1.2]]

        self.runner_book.update_traded(traded_update)
        assert self.runner_book.traded == traded_update

    def test_traded_update_fresh(self):
        traded_update = [[18.5, 1.2]]
        current = [[18, 297.39], [17.5, 369.53], [17, 222.05], [16.5, 290.74], [16, 1129.32], [15.5, 1858.49], [15, 3112.44], [14.5, 890.52], [9.8, 7.98], [14, 440.84], [13.5, 203.74], [13, 615.1], [12.5, 933.24], [11, 500.12], [10.5, 681.92], [10, 161.78], [12, 603.88], [11.5, 125.91]]
        self.runner_book.traded = current

        self.runner_book.update_traded(traded_update)
        current.append(traded_update[0])
        assert self.runner_book.traded == current

    def test_traded_update_addition(self):
        traded_update = [[17.5, 999.99], [16, 2001.00]]
        current = [[18, 297.39], [17.5, 369.53], [17, 222.05], [16.5, 290.74], [16, 1129.32], [15.5, 1858.49], [15, 3112.44], [14.5, 890.52], [9.8, 7.98], [14, 440.84], [13.5, 203.74], [13, 615.1], [12.5, 933.24], [11, 500.12], [10.5, 681.92], [10, 161.78], [12, 603.88], [11.5, 125.91]]
        self.runner_book.traded = current

        self.runner_book.update_traded(traded_update)
        expected = [[18, 297.39], [17.5, 999.99], [17, 222.05], [16.5, 290.74], [16, 2001.00], [15.5, 1858.49], [15, 3112.44], [14.5, 890.52], [9.8, 7.98], [14, 440.84], [13.5, 203.74], [13, 615.1], [12.5, 933.24], [11, 500.12], [10.5, 681.92], [10, 161.78], [12, 603.88], [11.5, 125.91]]
        assert self.runner_book.traded == expected
