import unittest
from tests import mock

from betfairlightweight.resources.streamingresources import (
    MarketDefinition, OrderBookCache, OrderBookRunner, UnmatchedOrder, MarketBookCache, RunnerBook, Available
)
from tests.tools import create_mock_json


class TestAvailable(unittest.TestCase):

    def setUp(self):
        self.prices = [[1, 1.02, 34.45], [0, 1.01, 12]]
        self.available = Available(self.prices, 2)

    def test_init(self):
        assert self.available.prices == self.prices
        assert self.available.deletion_select == 2
        assert self.available.reverse is False

    def test_sort(self):
        self.available.sort()
        assert self.available.prices == self.prices
        assert self.available.serialise == [{'price': 1.01, 'size': 12}, {'price': 1.02, 'size': 34.45}]

    def test_sort_short(self):
        current = [[27, 0.95], [13, 28.01], [1.02, 1157.21]]
        available = Available(current, 1)

        assert available.serialise == [
            {'price': 1.02, 'size': 1157.21}, {'price': 13, 'size': 28.01}, {'price': 27, 'size': 0.95}
        ]

    def test_clear(self):
        self.available.clear()
        assert self.available.prices == []

    def test_update_available_new_update(self):
        # [price, size]
        book_update = [[30, 6.9]]
        current = [[27, 0.95], [13, 28.01], [1.02, 1157.21]]
        expected = [[1.02, 1157.21],  [13, 28.01], [27, 0.95], [30, 6.9]]

        available = Available(current, 1)
        available.update(book_update)
        assert current == expected

        book_update = [[30, 6.9], [1.01, 12]]
        current = [[27, 0.95], [13, 28.01], [1.02, 1157.21]]
        expected = [[1.01, 12], [1.02, 1157.21], [13, 28.01], [27, 0.95], [30, 6.9]]

        available = Available(current, 1)
        available.update(book_update)
        assert current == expected

        # [position, price, size]
        book_update = [[0, 36, 0.57]]
        current = []
        expected = [[0, 36, 0.57]]

        available = Available(current, 2)
        available.update(book_update)
        assert available.prices == expected

    def test_update_available_new_replace(self):
        # [price, size]
        book_update = [[27, 6.9]]
        current = [[27, 0.95], [13, 28.01], [1.02, 1157.21]]
        expected = [[1.02, 1157.21], [13, 28.01], [27, 6.9]]

        available = Available(current, 1)
        available.update(book_update)
        assert current == expected

        # [position, price, size]
        book_update = [[0, 36, 0.57]]
        current = [[0, 36, 10.57], [1, 38, 3.57]]
        expected = [[0, 36, 0.57], [1, 38, 3.57]]

        available = Available(current, 2)
        available.update(book_update)
        assert current == expected

        # tests handling of betfair bug, http://forum.bdp.betfair.com/showthread.php?t=3351
        book_update = [[2, 0, 0], [1, 1.01, 9835.74], [0, 1.02, 1126.22]]
        current = [[1, 1.01, 9835.74], [0, 1.02, 1126.22]]
        expected = [[0, 1.02, 1126.22], [1, 1.01, 9835.74]]

        available = Available(current, 2)
        available.update(book_update)
        assert current == expected

    def test_update_available_new_remove(self):
        book_update = [[27, 0]]
        current = [[27, 0.95], [13, 28.01], [1.02, 1157.21]]
        expected = [[1.02, 1157.21], [13, 28.01]]

        available = Available(current, 1)
        available.update(book_update)
        assert current == expected

        # [position, price, size]
        book_update = [[0, 36, 0], [1, 38, 0], [0, 38, 3.57]]
        current = [[0, 36, 10.57], [1, 38, 3.57]]
        expected = [[0, 38, 3.57]]

        available = Available(current, 2)
        available.update(book_update)
        assert current == expected


class TestMarketDefinition(unittest.TestCase):

    def setUp(self):
        self.mock_response = create_mock_json('tests/resources/streaming_market_definition.json')
        self.market_definition = MarketDefinition(**self.mock_response.json())

    def test_init(self):
        assert len(self.market_definition.runners) == 7
        assert self.market_definition.bsp_market is True
        assert self.market_definition.market_base_rate == 5


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
            assert self.market_book_cache.market_definition == mock_market_definition(**book.get('marketDefinition'))

    @mock.patch('betfairlightweight.resources.streamingresources.MarketBookCache.strip_datetime')
    def test_update_cache_tv(self, mock_strip_datetime):
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
        market_book = self.market_book_cache.create_market_book(1234, {}, False)

        # assert market_book == mock_market_book(date_time_sent=self.market_book_cache._datetime_updated,
        #                                        streaming_unique_id=1234)()
        # mock_market_book.assert_called()

    def test_runner_dict(self):
        assert self.market_book_cache.runner_dict == {}

        class Runner:
            def __init__(self, selection_id, name):
                self.selection_id = selection_id
                self.name = name

        (a, b) = (Runner(123, 'a'), Runner(456, 'b'))
        self.market_book_cache.runners = [a, b]
        assert self.market_book_cache.runner_dict == {123: a, 456: b}

    # def test_market_definition_dict(self):
    #
    #     class Runner:
    #         def __init__(self, selection_id, name):
    #             self.id = selection_id
    #             self.name = name
    #
    #     (a, b) = (Runner(123, 'a'), Runner(456, 'b'))
    #     self.market_book_cache.market_definition = MarketDefinition(**{})
    #     self.market_book_cache.market_definition.runners = [a, b]
    #     assert self.market_book_cache.market_definition_dict == {123: a, 456: b}


class TestRunnerBook(unittest.TestCase):

    def setUp(self):
        self.runner_book = RunnerBook(**{'id': 123})

    def test_empty_serialise(self):
        runner_definition = mock.Mock()
        runner_definition.bsp = None
        serialise_d = self.runner_book.serialise(runner_definition)

        ex = serialise_d['ex']
        # all empty lists
        assert all(not ex[a] for a in ex.keys())

        sp = serialise_d['sp']
        # all 'None' or empty lists
        assert all(not sp[a] for a in sp.keys())



class TestOrderBookCache(unittest.TestCase):

    def setUp(self):
        self.order_book_cache = OrderBookCache(**{})
        self.runner = mock.Mock()
        self.runner.selection_id = 10895629
        self.runner.serialise_orders = mock.Mock(return_value=[])
        self.order_book_cache.runners = [self.runner]

    def test_update_cache(self):
        mock_response = create_mock_json('tests/resources/streaming_ocm_UPDATE.json')
        for order_book in mock_response.json().get('oc'):
            self.order_book_cache.update_cache(order_book, 1234)

            for order_changes in order_book.get('orc'):
                self.runner.update_matched_lays.assert_called_with(order_changes.get('ml', []))
                self.runner.update_matched_backs.assert_called_with(order_book.get('mb', []))
                self.runner.update_unmatched.assert_called_with(order_changes.get('uo', []))

    @mock.patch('betfairlightweight.resources.streamingresources.OrderBookRunner')
    def test_update_cache_new(self, mock_order_book_runner):
        self.runner.selection_id = 108956
        mock_response = create_mock_json('tests/resources/streaming_ocm_UPDATE.json')
        for order_book in mock_response.json().get('oc'):
            self.order_book_cache.update_cache(order_book, 1234)

            for order_changes in order_book.get('orc'):
                mock_order_book_runner.assert_called_with(**order_changes)

    @mock.patch('betfairlightweight.resources.streamingresources.OrderBookCache.serialise')
    @mock.patch('betfairlightweight.resources.streamingresources.CurrentOrders')
    def test_create_order_book(self, mock_current_orders, mock_serialise):
        current_orders = self.order_book_cache.create_order_book(123, {}, False)

        assert current_orders == mock_current_orders()

    def test_runner_dict(self):

        class Runner:
            def __init__(self, selection_id, name):
                self.selection_id = selection_id
                self.name = name

        (a, b) = (Runner(123, 'a'), Runner(456, 'b'))
        self.order_book_cache.runners = [a, b]
        assert self.order_book_cache.runner_dict == {123: a, 456: b}

    def test_serialise(self):
        serialised = self.order_book_cache.serialise

        assert serialised == {'currentOrders': [], 'moreAvailable': False}


class TestOrderBookRunner(unittest.TestCase):

    def setUp(self):
        self.order_book_runner = OrderBookRunner(**{'id': 1, 'ml': [], 'mb': [], 'uo': []})

    @mock.patch('betfairlightweight.resources.streamingresources.update_available')
    def test_update_matched_backs_fresh(self, mock_update_available):
        matched_backs = [[1.01, 4.00]]
        self.order_book_runner.update_matched_backs(matched_backs)

        assert len(self.order_book_runner.matched_backs) == 1

    @mock.patch('betfairlightweight.resources.streamingresources.update_available')
    def test_update_matched_backs_new(self, mock_update_available):
        mock_matched_back = mock.Mock()
        mock_matched_back.price = 1.01
        mock_matched_back.size = 2.00
        self.order_book_runner.matched_backs = [mock_matched_back]

        matched_backs = [[1.01, 4.00]]
        self.order_book_runner.update_matched_backs(matched_backs)

        mock_update_available.assert_called_with(self.order_book_runner.matched_backs, matched_backs, 1)
        assert len(self.order_book_runner.matched_backs) == 1

    @mock.patch('betfairlightweight.resources.streamingresources.update_available')
    def test_update_matched_lays_fresh(self, mock_update_available):
        mock_matched_lay = [[1.01, 4.00]]
        self.order_book_runner.update_matched_lays(mock_matched_lay)

        assert len(self.order_book_runner.matched_lays) == 1

    @mock.patch('betfairlightweight.resources.streamingresources.update_available')
    def test_update_matched_backs_new(self, mock_update_available):
        mock_matched_lay = mock.Mock()
        mock_matched_lay.price = 1.01
        mock_matched_lay.size = 2.00
        self.order_book_runner.matched_lays = [mock_matched_lay]

        matched_lays = [[1.01, 4.00]]
        self.order_book_runner.update_matched_lays(matched_lays)

        mock_update_available.assert_called_with(self.order_book_runner.matched_lays, matched_lays, 1)
        assert len(self.order_book_runner.matched_lays) == 1


class TestUnmatchedOrder(unittest.TestCase):

    def setUp(self):
        self.unmatched_order = UnmatchedOrder(**{})

    # def test_serialise(self):
    #     self.unmatched_order.serialise('1.23', 12345)
