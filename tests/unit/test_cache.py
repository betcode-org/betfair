import datetime
import unittest

from betfairlightweight.resources.baseresource import BaseResource
from betfairlightweight.streaming.cache import (
    OrderBookCache,
    OrderBookRunner,
    UnmatchedOrder,
    MarketBookCache,
    RunnerBook,
    Available,
    RaceCache,
)
from betfairlightweight.exceptions import CacheError
from tests import mock
from tests.unit.tools import create_mock_json


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


class TestMarketBookCache(unittest.TestCase):

    def setUp(self):
        self.market_book_cache = MarketBookCache(**{'marketDefinition': {'runners': {}}})

    def test_error(self):
        with self.assertRaises(CacheError):
            self.market_book_cache = MarketBookCache()

    @mock.patch('betfairlightweight.streaming.cache.MarketBookCache.strip_datetime')
    def test_update_cache_md(self, mock_strip_datetime):
        publish_time = mock.Mock()
        market_change = create_mock_json('tests/resources/streaming_mcm_UPDATE_md.json')
        book_data = market_change.json().get('mc')

        for book in book_data:
            self.market_book_cache.update_cache(book, publish_time)
            mock_strip_datetime.assert_called_with(publish_time)
            assert self.market_book_cache.market_definition == book.get('marketDefinition')

    @mock.patch('betfairlightweight.streaming.cache.MarketBookCache.strip_datetime')
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

    @mock.patch('betfairlightweight.streaming.cache.MarketBookCache.serialise')
    @mock.patch('betfairlightweight.streaming.cache.MarketDefinition')
    @mock.patch('betfairlightweight.streaming.cache.MarketBook')
    def test_create_resource(self, mock_market_book, mock_market_definition, mock_serialise):
        # lightweight
        market_book = self.market_book_cache.create_resource(1234, {}, True)
        assert market_book == mock_serialise
        # not lightweight
        market_book = self.market_book_cache.create_resource(1234, {}, False)
        assert market_book == mock_market_book()

    def test_update_runner_dict(self):
        assert self.market_book_cache.runner_dict == {}

        class Runner:
            def __init__(self, selection_id, name, handicap):
                self.selection_id = selection_id
                self.name = name
                self.handicap = handicap

        (a, b) = (Runner(123, 'a', 1.25), Runner(456, 'b', -0.25))
        self.market_book_cache.runners = [a, b]
        self.market_book_cache._update_runner_dict()
        assert self.market_book_cache.runner_dict == {(123, 1.25): a, (456, -0.25): b}

    def test_init_multiple_rc(self):
        # Initialize data with multiple rc entries for the same selection
        data = {'marketDefinition': {'runners': {}}}
        data['rc'] = [{'atb': [[1.01, 200]], 'id': 13536143}, {'atl': [[1000.0, 200]], 'id': 13536143}]

        market_book_cache = MarketBookCache(**data)

        assert len(market_book_cache.runners) == len(market_book_cache.runner_dict)


class TestRunnerBook(unittest.TestCase):

    def setUp(self):
        self.runner_book = RunnerBook(**{'id': 123})

    def test_update_traded(self):
        self.mock_traded = mock.Mock()
        self.runner_book.traded = self.mock_traded

        self.runner_book.update_traded([])
        self.mock_traded.clear.assert_called_with()

        self.runner_book.update_traded([1, 2])
        self.mock_traded.update.assert_called_with([1, 2])

    def test_serialise_back(self):
        mock_available_to_back = mock.Mock()
        mock_available_to_back.prices = True
        mock_best_available_to_back = mock.Mock()
        mock_best_available_to_back.prices = True
        mock_best_display_available_to_back = mock.Mock()
        mock_best_display_available_to_back.prices = True
        self.runner_book.available_to_back = mock_available_to_back

        assert self.runner_book.serialise_available_to_back() == mock_available_to_back.serialise

        mock_available_to_back.prices = False
        self.runner_book.best_available_to_back = mock_best_available_to_back
        assert self.runner_book.serialise_available_to_back() == mock_best_available_to_back.serialise

        mock_best_available_to_back.prices = False
        self.runner_book.best_display_available_to_back = mock_best_display_available_to_back
        assert self.runner_book.serialise_available_to_back() == mock_best_display_available_to_back.serialise

    def test_serialise_lay(self):
        mock_available_to_lay = mock.Mock()
        mock_available_to_lay.prices = True
        mock_best_available_to_lay = mock.Mock()
        mock_best_available_to_lay.prices = True
        mock_best_display_available_to_lay = mock.Mock()
        mock_best_display_available_to_lay.prices = True
        self.runner_book.available_to_lay = mock_available_to_lay

        assert self.runner_book.serialise_available_to_lay() == mock_available_to_lay.serialise

        mock_available_to_lay.prices = False
        self.runner_book.best_available_to_lay = mock_best_available_to_lay
        assert self.runner_book.serialise_available_to_lay() == mock_best_available_to_lay.serialise

        mock_best_available_to_lay.prices = False
        self.runner_book.best_display_available_to_lay = mock_best_display_available_to_lay
        assert self.runner_book.serialise_available_to_lay() == mock_best_display_available_to_lay.serialise

    def test_empty_serialise(self):
        runner_definition = {
            'bdp': None,
        }
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
                # self.runner.matched_lays.update.assert_called_with(order_changes.get('ml', []))
                # self.runner.matched_backs.update.assert_called_with(order_book.get('mb', []))
                self.runner.update_unmatched.assert_called_with(order_changes.get('uo', []))

    @mock.patch('betfairlightweight.streaming.cache.OrderBookRunner')
    def test_update_cache_new(self, mock_order_book_runner):
        self.runner.selection_id = 108956
        mock_response = create_mock_json('tests/resources/streaming_ocm_UPDATE.json')
        for order_book in mock_response.json().get('oc'):
            self.order_book_cache.update_cache(order_book, 1234)

            for order_changes in order_book.get('orc'):
                mock_order_book_runner.assert_called_with(**order_changes)

    @mock.patch('betfairlightweight.streaming.cache.OrderBookCache.serialise')
    @mock.patch('betfairlightweight.streaming.cache.CurrentOrders')
    def test_create_resource(self, mock_current_orders, mock_serialise):
        current_orders = self.order_book_cache.create_resource(123, {}, False)

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


class TestUnmatchedOrder(unittest.TestCase):

    def setUp(self):
        order = {
            'id': 1, 'p': 2, 's': 3, 'side': 'L', 'status': 'E', 'pt': 'L', 'ot': 'L', 'pd': 8, 'sm': 9, 'sr': 10,
            'sl': 11, 'sc': 12, 'sv': 13, 'rfo': 14, 'rfs': 15, 'ld': 16, 'lsrc': 17, 'error': 'test'
        }
        self.unmatched_order = UnmatchedOrder(**order)

    def test_init(self):
        assert self.unmatched_order.bet_id == 1
        assert self.unmatched_order.price == 2
        assert self.unmatched_order.size == 3
        assert self.unmatched_order.side == 'L'
        assert self.unmatched_order.status == 'E'
        assert self.unmatched_order.persistence_type == 'L'
        assert self.unmatched_order.order_type == 'L'
        assert self.unmatched_order.placed_date == BaseResource.strip_datetime(8)
        assert self.unmatched_order.size_matched == 9
        assert self.unmatched_order.size_remaining == 10
        assert self.unmatched_order.size_lapsed == 11
        assert self.unmatched_order.size_cancelled == 12
        assert self.unmatched_order.size_voided == 13
        assert self.unmatched_order.reference_order == 14
        assert self.unmatched_order.reference_strategy == 15
        assert self.unmatched_order.lapsed_date == 16
        assert self.unmatched_order.lapse_status_reason_code == 17

    def test_placed_date_string(self):
        now = datetime.datetime.now()
        self.unmatched_order.placed_date = now
        assert self.unmatched_order.placed_date_string == now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    def test_matched_date_string(self):
        now = datetime.datetime.now()
        self.unmatched_order.matched_date = now
        assert self.unmatched_order.matched_date_string == now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    def test_serialise(self):
        assert self.unmatched_order.serialise('1.23', 12345, 0.0) == {
            'sizeLapsed': 11, 'persistenceType': 'LAPSE', 'sizeRemaining': 10,
            'placedDate': '1970-01-01T00:00:00.008000Z', 'sizeVoided': 13, 'sizeCancelled': 12, 'betId': 1,
            'customerOrderRef': 14, 'orderType': 'LIMIT', 'marketId': '1.23', 'matchedDate': None, 'side': 'LAY',
            'selectionId': 12345, 'bspLiability': None, 'sizeMatched': 9, 'handicap': 0.0, 'averagePriceMatched': 0.0,
            'status': 'EXECUTABLE', 'customerStrategyRef': 15, 'regulatorCode': None,
            'priceSize': {'price': 2, 'size': 3}
        }


class TestRaceCache(unittest.TestCase):

    def setUp(self):
        update = {'mid': "1.12", "id": "12.12"}
        self.race_cache = RaceCache(**update)

    def test_init(self):
        assert self.race_cache.publish_time is None
        assert self.race_cache.rpc is None
        assert self.race_cache.rrc == []

    def test_update_rpm(self):
        update = {'rpc': 1234}
        publish_time = 1518626764
        self.race_cache.update_cache(update, publish_time)

        assert self.race_cache._datetime_updated is not None
        assert self.race_cache.publish_time == publish_time
        assert self.race_cache.rpc == 1234

    def test_update_rrc(self):
        update = {'rrc': [{'id': 1}]}
        publish_time = 1518626764
        self.race_cache.update_cache(update, publish_time)

        assert self.race_cache._datetime_updated is not None
        assert self.race_cache.publish_time == publish_time
        assert len(self.race_cache.rrc) == 1

    @mock.patch('betfairlightweight.streaming.cache.RaceCache.serialise')
    def test_create_resource_lightweight(self, mock_serialise):
        assert self.race_cache.create_resource(12, {}, True) == mock_serialise

    # @mock.patch('betfairlightweight.streaming.cache.Race')
    # @mock.patch('betfairlightweight.streaming.cache.RaceCache.serialise')
    # def test_create_resource(self, mock_serialise, mock_race):
    #     # print(self.race_cache.create_resource(12, {}, False))
    #     self.assertIsInstance(self.race_cache.create_resource(12, {}, False), mock_race)

    def test_serialise(self):
        self.race_cache.rpc = {'test': 123}
        mock_runner = mock.Mock()
        mock_runner.change = {'test': 'me'}
        self.race_cache.rrc = [mock_runner]
        self.race_cache.publish_time = 12
        assert self.race_cache.serialise == {
            'pt': 12,
            'mid': '1.12',
            'id': '12.12',
            'rpc': {'test': 123},
            'rrc': [{'test': 'me'}]
        }
