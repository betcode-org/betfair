import unittest
from unittest import mock

from betfairlightweight.resources.streamingresources import (
    MarketDefinition, OrderBookCache, OrderBookRunner, Matched, UnmatchedOrder
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
