import unittest
from unittest import mock

from betfairlightweight.resources.baseresource import BaseResource
from betfairlightweight.streaming.cache import (
    OrderBookCache,
    OrderBookRunner,
    UnmatchedOrder,
    MarketBookCache,
    RunnerBookCache,
    Available,
    RaceCache,
)
from tests.unit.tools import create_mock_json


class TestAvailable(unittest.TestCase):
    def setUp(self):
        self.prices = [[1, 1.02, 34.45], [0, 1.01, 12]]
        self.available = Available(self.prices, 2)

    def test_init(self):
        self.assertEqual(
            self.available.order_book,
            {
                0: [0, 1.01, 12, {"price": 1.01, "size": 12}],
                1: [1, 1.02, 34.45, {"price": 1.02, "size": 34.45}],
            },
        )
        self.assertEqual(self.available.deletion_select, 2)
        self.assertFalse(self.available.reverse)
        self.assertEqual(
            self.available.serialised,
            [{"price": 1.01, "size": 12}, {"price": 1.02, "size": 34.45}],
        )

    def test_serialise(self):
        # [price, size]
        current = [[27, 0.95], [13, 28.01], [1.02, 1157.21]]
        available = Available(current, 1)
        available.serialise()
        self.assertEqual(
            available.serialised,
            [
                {"price": 1.02, "size": 1157.21},
                {"price": 13, "size": 28.01},
                {"price": 27, "size": 0.95},
            ],
        )

        # [position, price, size]
        current = [[2, 27, 0.95], [1, 13, 28.01], [0, 1.02, 1157.21]]
        available = Available(current, 2)
        available.serialise()
        self.assertEqual(
            available.serialised,
            [
                {"price": 1.02, "size": 1157.21},
                {"price": 13, "size": 28.01},
                {"price": 27, "size": 0.95},
            ],
        )

    @mock.patch("betfairlightweight.streaming.cache.Available.serialise")
    def test_clear(self, mock_serialise):
        self.available.clear()
        assert self.available.order_book == {}
        mock_serialise.assert_called()

    def test__sort_order_book(self):
        self.available.order_book = {1.01: [2], 100: [3], 13: [5]}
        self.available._sort_order_book()
        self.assertEqual(list(self.available.order_book.keys()), [1.01, 13, 100])
        # reverse
        self.available.reverse = True
        self.available._sort_order_book()
        self.assertEqual(list(self.available.order_book.keys()), [100, 13, 1.01])

    @mock.patch("betfairlightweight.streaming.cache.Available.serialise")
    def test_update(self, mock_serialise):
        book_update = [[27, 2]]  # [price, size]
        current = [[27, 0.95], [13, 28.01], [1.02, 1157.21]]
        expected = {
            27: [27, 2, {"price": 27, "size": 2}],
            13: [13, 28.01, {"price": 13, "size": 28.01}],
            1.02: [1.02, 1157.21, {"price": 1.02, "size": 1157.21}],
        }

        available = Available(current, 1)
        available.update(book_update)
        mock_serialise.assert_called()
        self.assertEqual(available.order_book, expected)

    @mock.patch("betfairlightweight.streaming.cache.Available._sort_order_book")
    @mock.patch("betfairlightweight.streaming.cache.Available.serialise")
    def test_update_new(self, mock_serialise, mock__sort_order_book):
        book_update = [[30, 6.9]]  # [price, size]
        current = [[27, 0.95], [13, 28.01], [1.02, 1157.21]]
        expected = {
            27: [27, 0.95, {"price": 27, "size": 0.95}],
            13: [13, 28.01, {"price": 13, "size": 28.01}],
            1.02: [1.02, 1157.21, {"price": 1.02, "size": 1157.21}],
            30: [30, 6.9, {"price": 30, "size": 6.9}],
        }

        available = Available(current, 1)
        available.update(book_update)
        mock_serialise.assert_called()
        mock__sort_order_book.assert_called()
        self.assertEqual(available.order_book, expected)

    @mock.patch("betfairlightweight.streaming.cache.Available.serialise")
    def test_update_del(self, mock_serialise):
        book_update = [[27, 0]]  # [price, size]
        current = [[27, 0.95], [13, 28.01], [1.02, 1157.21]]
        expected = {
            13: [13, 28.01, {"price": 13, "size": 28.01}],
            1.02: [1.02, 1157.21, {"price": 1.02, "size": 1157.21}],
        }

        available = Available(current, 1)
        available.update(book_update)
        mock_serialise.assert_called()
        self.assertEqual(available.order_book, expected)

    @mock.patch("betfairlightweight.streaming.cache.Available._sort_order_book")
    @mock.patch("betfairlightweight.streaming.cache.Available.serialise")
    def test_update_available_new_update(self, mock_serialise, mock__sort_order_book):
        # [price, size]
        book_update = [[30, 6.9]]
        current = [[27, 0.95], [13, 28.01], [1.02, 1157.21]]
        expected = {
            27: [27, 0.95, {"price": 27, "size": 0.95}],
            13: [13, 28.01, {"price": 13, "size": 28.01}],
            1.02: [1.02, 1157.21, {"price": 1.02, "size": 1157.21}],
            30: [30, 6.9, {"price": 30, "size": 6.9}],
        }
        available = Available(current, 1)
        available.update(book_update)
        assert available.order_book == expected

        book_update = [[30, 6.9], [1.01, 12]]
        current = [[27, 0.95], [13, 28.01], [1.02, 1157.21]]
        expected = {
            27: [27, 0.95, {"price": 27, "size": 0.95}],
            13: [13, 28.01, {"price": 13, "size": 28.01}],
            1.02: [1.02, 1157.21, {"price": 1.02, "size": 1157.21}],
            1.01: [1.01, 12, {"price": 1.01, "size": 12}],
            30: [30, 6.9, {"price": 30, "size": 6.9}],
        }
        available = Available(current, 1)
        available.update(book_update)
        assert available.order_book == expected

        # [position, price, size]
        book_update = [[0, 36, 0.57]]
        current = []
        expected = {0: [0, 36, 0.57, {"price": 36, "size": 0.57}]}
        available = Available(current, 2)
        available.update(book_update)
        assert available.order_book == expected

    @mock.patch("betfairlightweight.streaming.cache.Available._sort_order_book")
    @mock.patch("betfairlightweight.streaming.cache.Available.serialise")
    def test_update_available_new_replace(self, mock_serialise, mock__sort_order_book):
        # [price, size]
        book_update = [[27, 6.9]]
        current = [[27, 0.95], [13, 28.01], [1.02, 1157.21]]
        expected = {
            27: [27, 6.9, {"price": 27, "size": 6.9}],
            13: [13, 28.01, {"price": 13, "size": 28.01}],
            1.02: [1.02, 1157.21, {"price": 1.02, "size": 1157.21}],
        }
        available = Available(current, 1)
        available.update(book_update)
        assert available.order_book == expected

        # [position, price, size]
        book_update = [[0, 36, 0.57]]
        current = [[0, 36, 10.57], [1, 38, 3.57]]
        expected = {
            0: [0, 36, 0.57, {"price": 36, "size": 0.57}],
            1: [1, 38, 3.57, {"price": 38, "size": 3.57}],
        }
        available = Available(current, 2)
        available.update(book_update)
        assert available.order_book == expected

        # tests handling of betfair bug, http://forum.bdp.betfair.com/showthread.php?t=3351
        book_update = [[2, 0, 0], [1, 1.01, 9835.74], [0, 1.02, 1126.22]]
        current = [[1, 1.01, 9835.74], [0, 1.02, 1126.22]]
        expected = {
            0: [0, 1.02, 1126.22, {"price": 1.02, "size": 1126.22}],
            1: [1, 1.01, 9835.74, {"price": 1.01, "size": 9835.74}],
        }
        available = Available(current, 2)
        available.update(book_update)
        assert available.order_book == expected

    @mock.patch("betfairlightweight.streaming.cache.Available._sort_order_book")
    @mock.patch("betfairlightweight.streaming.cache.Available.serialise")
    def test_update_available_new_remove(self, mock_serialise, mock__sort_order_book):
        # [price, size]
        book_update = [[27, 0]]
        current = [[27, 0.95], [13, 28.01], [1.02, 1157.21]]
        expected = {
            1.02: [1.02, 1157.21, {"price": 1.02, "size": 1157.21}],
            13: [13, 28.01, {"price": 13, "size": 28.01}],
        }
        available = Available(current, 1)
        available.update(book_update)
        assert available.order_book == expected

        # [position, price, size]
        book_update = [[0, 36, 0], [1, 38, 0], [0, 38, 3.57]]
        current = [[0, 36, 10.57], [1, 38, 3.57]]
        expected = {0: [0, 38, 3.57, {"price": 38, "size": 3.57}]}
        available = Available(current, 2)
        available.update(book_update)
        assert available.order_book == expected


class TestMarketBookCache(unittest.TestCase):
    def setUp(self):
        self.market_book_cache = MarketBookCache("1.2345", 12345, True)

    def test_init(self):
        self.assertEqual(self.market_book_cache.market_id, "1.2345")
        self.assertEqual(self.market_book_cache.publish_time, 12345)
        self.assertTrue(self.market_book_cache.lightweight)
        self.assertIsNone(self.market_book_cache.total_matched)
        self.assertEqual(self.market_book_cache.market_definition, {})
        self.assertIsNone(self.market_book_cache._market_definition_resource)
        self.assertIsNone(self.market_book_cache._definition_bet_delay)
        self.assertIsNone(self.market_book_cache._definition_version)
        self.assertIsNone(self.market_book_cache._definition_complete)
        self.assertIsNone(self.market_book_cache._definition_runners_voidable)
        self.assertIsNone(self.market_book_cache._definition_status)
        self.assertIsNone(self.market_book_cache._definition_bsp_reconciled)
        self.assertIsNone(self.market_book_cache._definition_cross_matching)
        self.assertIsNone(self.market_book_cache._definition_in_play)
        self.assertIsNone(self.market_book_cache._definition_number_of_winners)
        self.assertIsNone(self.market_book_cache._definition_number_of_active_runners)
        self.assertIsNone(self.market_book_cache._definition_price_ladder_definition)
        self.assertIsNone(self.market_book_cache._definition_key_line_description)
        self.assertIsNone(self.market_book_cache.streaming_update)
        self.assertEqual(self.market_book_cache.runners, [])
        self.assertEqual(self.market_book_cache.runner_dict, {})
        self.assertEqual(self.market_book_cache._number_of_runners, 0)

    @mock.patch("betfairlightweight.streaming.cache.MarketBookCache.strip_datetime")
    def test_update_cache_md(self, mock_strip_datetime):
        publish_time = mock.Mock()
        market_change = create_mock_json("tests/resources/streaming_mcm_UPDATE_md.json")
        book_data = market_change.json().get("mc")

        for book in book_data:
            self.market_book_cache.update_cache(book, publish_time)
            assert self.market_book_cache.market_definition == book.get(
                "marketDefinition"
            )
            self.assertEqual(self.market_book_cache.streaming_update, book)

    @mock.patch("betfairlightweight.streaming.cache.MarketBookCache.strip_datetime")
    def test_update_cache_tv(self, mock_strip_datetime):
        publish_time = mock.Mock()
        market_change = create_mock_json("tests/resources/streaming_mcm_UPDATE_tv.json")
        book_data = market_change.json().get("mc")

        for book in book_data:
            self.market_book_cache.update_cache(book, publish_time)
            assert self.market_book_cache.total_matched == book.get("tv")
            self.assertEqual(self.market_book_cache.streaming_update, book)

    def test_update_multiple_rc(self):
        # update data with multiple rc entries for the same selection
        data = {
            "rc": [
                {"atb": [[1.01, 200]], "id": 13536143},
                {"atl": [[1000.0, 200]], "id": 13536143},
            ]
        }

        market_book_cache = MarketBookCache("1.123", 123, True)
        market_book_cache.update_cache(data, 123)

        assert len(market_book_cache.runners) == len(market_book_cache.runner_dict)

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

    @mock.patch(
        "betfairlightweight.streaming.cache.MarketBookCache.serialise",
        new_callable=mock.PropertyMock,
        return_value={},
    )
    @mock.patch("betfairlightweight.streaming.cache.MarketDefinition")
    @mock.patch("betfairlightweight.streaming.cache.MarketBook")
    def test_create_resource(
        self, mock_market_book, mock_market_definition, mock_serialise
    ):
        # lightweight
        market_book = self.market_book_cache.create_resource(1234, True)
        assert market_book == {
            "streaming_unique_id": 1234,
            "streaming_snap": True,
        }
        assert market_book == mock_serialise()
        # not lightweight
        self.market_book_cache.lightweight = False
        market_book = self.market_book_cache.create_resource(1234, True)
        assert market_book == mock_market_book()

    @mock.patch(
        "betfairlightweight.streaming.cache.MarketBookCache.serialise",
        new_callable=mock.PropertyMock,
        return_value={},
    )
    @mock.patch("betfairlightweight.streaming.cache.MarketDefinition")
    @mock.patch("betfairlightweight.streaming.cache.MarketBook")
    def test_create_resource_snap(self, *_):
        market_book = self.market_book_cache.create_resource(1234, True)
        assert market_book == {
            "streaming_unique_id": 1234,
            "streaming_snap": True,
        }

    @mock.patch("betfairlightweight.streaming.cache.MarketBook")
    def test_create_resource_resource(self, mock_market_book):
        self.market_book_cache.lightweight = False
        self.assertEqual(
            self.market_book_cache.create_resource(1, False), mock_market_book()
        )
        # todo

    @mock.patch("betfairlightweight.streaming.cache.MarketDefinition")
    @mock.patch("betfairlightweight.streaming.cache.MarketBookCache._add_new_runner")
    def test__process_market_definition(
        self, mock__add_new_runner, mock_market_definition_cls
    ):
        self.market_book_cache.lightweight = False
        mock_market_definition = {"runners": [{"id": 12}]}
        self.market_book_cache._process_market_definition(mock_market_definition)

        self.assertEqual(
            self.market_book_cache.market_definition, mock_market_definition
        )
        self.assertEqual(self.market_book_cache.runner_dict, {})
        mock__add_new_runner.assert_called_with(id=12, hc=0, definition={"id": 12})
        mock__add_new_runner().serialise.assert_called()

        mock_market_definition = {"runners": [{"id": 34, "hc": 1}]}
        self.market_book_cache._process_market_definition(mock_market_definition)

        self.assertEqual(
            self.market_book_cache.market_definition, mock_market_definition
        )
        self.assertEqual(self.market_book_cache.runner_dict, {})
        mock__add_new_runner.assert_called_with(
            id=34, hc=1, definition={"id": 34, "hc": 1}
        )
        mock__add_new_runner().serialise.assert_called()
        mock_market_definition_cls.assert_called_with(**mock_market_definition)
        self.assertEqual(
            self.market_book_cache._market_definition_resource,
            mock_market_definition_cls(),
        )

    @mock.patch("betfairlightweight.streaming.cache.MarketDefinition")
    def test__process_market_definition_caches(self, mock_market_definition_cls):
        mock_market_definition = {
            "betDelay": 1,
            "version": 234,
            "complete": True,
            "runnersVoidable": False,
            "status": "ACTIVE",
            "bspReconciled": True,
            "crossMatching": False,
            "inPlay": True,
            "numberOfWinners": 5,
            "numberOfActiveRunners": 6,
            "priceLadderDefinition": "",
        }
        self.market_book_cache._process_market_definition(mock_market_definition)

        self.assertEqual(self.market_book_cache._definition_bet_delay, 1)
        self.assertEqual(self.market_book_cache._definition_version, 234)
        self.assertEqual(self.market_book_cache._definition_complete, True)
        self.assertEqual(self.market_book_cache._definition_runners_voidable, False)
        self.assertEqual(self.market_book_cache._definition_status, "ACTIVE")
        self.assertEqual(self.market_book_cache._definition_bsp_reconciled, True)
        self.assertEqual(self.market_book_cache._definition_cross_matching, False)
        self.assertEqual(self.market_book_cache._definition_in_play, True)
        self.assertEqual(self.market_book_cache._definition_number_of_winners, 5)
        self.assertEqual(self.market_book_cache._definition_number_of_active_runners, 6)
        self.assertEqual(self.market_book_cache._definition_price_ladder_definition, "")
        self.assertEqual(self.market_book_cache._definition_key_line_description, None)

    @mock.patch("betfairlightweight.streaming.cache.RunnerBookCache")
    def test__add_new_runner(self, mock_runner_book_cache):
        self.assertEqual(self.market_book_cache.runner_dict, {})
        self.market_book_cache._add_new_runner(id=1, hc=2, definition={1: 2})
        mock_runner_book_cache.assert_called_with(
            lightweight=True, id=1, hc=2, definition={1: 2}
        )
        self.assertEqual(
            self.market_book_cache.runner_dict,
            {
                (
                    mock_runner_book_cache().selection_id,
                    mock_runner_book_cache().handicap,
                ): mock_runner_book_cache()
            },
        )
        self.assertEqual(self.market_book_cache.runners, [mock_runner_book_cache()])
        self.assertEqual(self.market_book_cache._number_of_runners, 1)

    def test_closed(self):
        self.assertFalse(self.market_book_cache.closed)
        self.market_book_cache.market_definition = {"status": "CLOSED"}
        self.assertTrue(self.market_book_cache.closed)


class TestRunnerBookCache(unittest.TestCase):
    def setUp(self):
        self.runner_book = RunnerBookCache(lightweight=True, **{"id": 123})

    def test_init(self):
        self.assertEqual(self.runner_book.selection_id, 123)
        self.assertTrue(self.runner_book.lightweight)
        self.assertEqual(self.runner_book.serialised, {})
        self.assertIsNone(self.runner_book.resource)

    def test_update_definition(self):
        definition = {
            "status": "ACTIVE",
            "bsp": 12,
            "adjustmentFactor": 23.1,
        }
        self.runner_book.update_definition(definition)
        self.assertEqual(self.runner_book.definition, definition)
        self.assertEqual(self.runner_book._definition_status, "ACTIVE")
        self.assertEqual(self.runner_book._definition_bsp, 12)
        self.assertEqual(self.runner_book._definition_adjustment_factor, 23.1)
        self.assertIsNone(self.runner_book._definition_removal_date)

    def test_update_traded(self):
        self.mock_traded = mock.Mock()
        self.runner_book.traded = self.mock_traded

        self.runner_book.update_traded([])
        self.mock_traded.clear.assert_called_with()

        self.runner_book.update_traded([1, 2])
        self.mock_traded.update.assert_called_with([1, 2])

    def test_serialise_back(self):
        mock_available_to_back = mock.Mock()
        mock_available_to_back.order_book = True
        mock_best_available_to_back = mock.Mock()
        mock_best_available_to_back.prices = True
        mock_best_display_available_to_back = mock.Mock()
        mock_best_display_available_to_back.order_book = True
        self.runner_book.available_to_back = mock_available_to_back

        assert (
            self.runner_book.serialise_available_to_back()
            == mock_available_to_back.serialised
        )

        mock_available_to_back.order_book = False
        self.runner_book.best_available_to_back = mock_best_available_to_back
        assert (
            self.runner_book.serialise_available_to_back()
            == mock_best_available_to_back.serialised
        )

        mock_best_available_to_back.order_book = False
        self.runner_book.best_display_available_to_back = (
            mock_best_display_available_to_back
        )
        assert (
            self.runner_book.serialise_available_to_back()
            == mock_best_display_available_to_back.serialised
        )

    def test_serialise_lay(self):
        mock_available_to_lay = mock.Mock()
        mock_available_to_lay.order_book = True
        mock_best_available_to_lay = mock.Mock()
        mock_best_available_to_lay.prices = True
        mock_best_display_available_to_lay = mock.Mock()
        mock_best_display_available_to_lay.order_book = True
        self.runner_book.available_to_lay = mock_available_to_lay

        assert (
            self.runner_book.serialise_available_to_lay()
            == mock_available_to_lay.serialised
        )

        mock_available_to_lay.order_book = False
        self.runner_book.best_available_to_lay = mock_best_available_to_lay
        assert (
            self.runner_book.serialise_available_to_lay()
            == mock_best_available_to_lay.serialised
        )

        mock_best_available_to_lay.order_book = False
        self.runner_book.best_display_available_to_lay = (
            mock_best_display_available_to_lay
        )
        assert (
            self.runner_book.serialise_available_to_lay()
            == mock_best_display_available_to_lay.serialised
        )

    def test_serialise(self):
        self.runner_book._definition_status = "ACTIVE"
        self.runner_book._definition_bsp = 12
        self.runner_book._definition_adjustment_factor = 23.1
        self.runner_book.serialise()
        self.assertEqual(
            self.runner_book.serialised,
            {
                "adjustmentFactor": 23.1,
                "ex": {"availableToBack": [], "availableToLay": [], "tradedVolume": []},
                "handicap": 0,
                "lastPriceTraded": None,
                "removalDate": None,
                "selectionId": 123,
                "sp": {
                    "actualSP": 12,
                    "backStakeTaken": [],
                    "farPrice": None,
                    "layLiabilityTaken": [],
                    "nearPrice": None,
                },
                "status": "ACTIVE",
                "totalMatched": None,
            },
        )

    def test_empty_serialise(self):
        self.runner_book.serialise()

        ex = self.runner_book.serialised["ex"]
        # all empty lists
        assert all(not ex[a] for a in ex.keys())

        sp = self.runner_book.serialised["sp"]
        # all 'None' or empty lists
        assert all(not sp[a] for a in sp.keys())

    @mock.patch("betfairlightweight.streaming.cache.RunnerBook")
    def test_serialise_resource(self, mock_runner_book):
        self.runner_book.lightweight = False
        self.runner_book.serialise()
        mock_runner_book.assert_called_with(**self.runner_book.serialised)
        self.assertEqual(self.runner_book.resource, mock_runner_book())


class TestOrderBookCache(unittest.TestCase):
    def setUp(self):
        self.order_book_cache = OrderBookCache("1.123", 123, True)
        self.runner = mock.Mock()
        self.runner.selection_id = 10895629
        self.runner.handicap = 0
        self.runner.serialise_orders = mock.Mock(return_value=[])
        self.runner.unmatched_orders = [1]
        self.order_book_cache.runners = {(10895629, 0): self.runner}

    def test_init(self):
        self.assertEqual(self.order_book_cache.market_id, "1.123")
        self.assertEqual(self.order_book_cache.publish_time, 123)
        self.assertTrue(self.order_book_cache.lightweight)

    def test_full_image(self):
        self.order_book_cache.runners = {}
        mock_response = create_mock_json(
            "tests/resources/streaming_ocm_FULL_IMAGE.json"
        )
        for order_book in mock_response.json().get("oc"):
            self.order_book_cache.update_cache(order_book, 1234)
            self.assertEqual(self.order_book_cache.streaming_update, order_book)

        self.assertEqual(len(self.order_book_cache.runners), 5)
        for k, v in self.order_book_cache.runners.items():
            self.assertEqual(len(v.unmatched_orders), 1)

    def test_update_cache(self):
        mock_response = create_mock_json("tests/resources/streaming_ocm_UPDATE.json")
        for order_book in mock_response.json().get("oc"):
            self.order_book_cache.update_cache(order_book, 1234)
            self.assertEqual(self.order_book_cache.streaming_update, order_book)

            for order_changes in order_book.get("orc"):
                # self.runner.matched_lays.update.assert_called_with(order_changes.get('ml', []))
                # self.runner.matched_backs.update.assert_called_with(order_book.get('mb', []))
                self.runner.update_unmatched.assert_called_with(
                    order_changes.get("uo", [])
                )

    @mock.patch("betfairlightweight.streaming.cache.OrderBookRunner")
    def test_update_cache_new(self, mock_order_book_runner):
        self.order_book_cache.runners = {(108956, 0): self.runner}
        mock_response = create_mock_json("tests/resources/streaming_ocm_UPDATE.json")
        for order_book in mock_response.json().get("oc"):
            self.order_book_cache.update_cache(order_book, 1234)
            self.assertEqual(self.order_book_cache.streaming_update, order_book)

            for order_changes in order_book.get("orc"):
                mock_order_book_runner.assert_called_with(
                    self.order_book_cache.market_id, **order_changes
                )

    def test_update_cache_closed(self):
        mock_response = create_mock_json("tests/resources/streaming_ocm_SUB_IMAGE.json")
        for order_book in mock_response.json().get("oc"):
            self.order_book_cache.update_cache(order_book, 1234)
            self.assertEqual(self.order_book_cache.streaming_update, order_book)
        self.assertTrue(self.order_book_cache.closed)

    @mock.patch(
        "betfairlightweight.streaming.cache.OrderBookCache.serialise",
        new_callable=mock.PropertyMock,
        return_value={},
    )
    @mock.patch("betfairlightweight.streaming.cache.CurrentOrders")
    def test_create_resource(self, mock_current_orders, mock_serialise):
        # lightweight
        current_orders = self.order_book_cache.create_resource(123, True)
        assert current_orders == mock_serialise()
        assert current_orders == {
            "streaming_unique_id": 123,
            "streaming_snap": True,
        }
        # not lightweight
        self.order_book_cache.lightweight = False
        current_orders = self.order_book_cache.create_resource(123, True)
        assert current_orders == mock_current_orders()

    def test_serialise(self):
        mock_runner_one = mock.Mock()
        mock_runner_one.serialise_orders.return_value = [1]
        mock_runner_one.serialise_matches.return_value = 6
        mock_runner_two = mock.Mock()
        mock_runner_two.serialise_orders.return_value = [2, 3]
        mock_runner_two.serialise_matches.return_value = 4
        self.order_book_cache.runners = {
            (123, 0): mock_runner_one,
            (123, 1): mock_runner_two,
        }
        serialised = self.order_book_cache.serialise
        self.assertEqual(
            serialised,
            {
                "currentOrders": [1, 2, 3],
                "matches": [6, 4],
                "moreAvailable": False,
                "streaming_update": None,
            },
        )


class TestOrderBookRunner(unittest.TestCase):
    def setUp(self):
        uo = [
            {
                "id": 1,
                "p": "a",
                "s": "a",
                "side": "L",
                "ot": "L",
                "pd": "a",
                "sm": "a",
                "sr": "a",
                "sl": "a",
                "sc": "a",
                "sv": "a",
                "rfo": "a",
                "rfs": "a",
                "status": "E",
            },
            {
                "id": 2,
                "p": "b",
                "s": "a",
                "side": "L",
                "ot": "L",
                "pd": "a",
                "sm": "a",
                "sr": "a",
                "sl": "a",
                "sc": "a",
                "sv": "a",
                "rfo": "a",
                "rfs": "a",
                "status": "EC",
            },
        ]
        self.order_book_runner = OrderBookRunner(
            "1.123", **{"id": 1, "ml": [], "mb": [], "uo": uo}
        )

    def test_init(self):
        self.assertEqual(self.order_book_runner.market_id, "1.123")
        self.assertEqual(self.order_book_runner.selection_id, 1)
        self.assertEqual(self.order_book_runner.handicap, 0)
        self.assertIsNone(self.order_book_runner.full_image)
        self.assertIsNone(self.order_book_runner.strategy_matches)
        self.assertEqual(len(self.order_book_runner.unmatched_orders), 2)

    def test_update_unmatched(self):
        unmatched_orders = [
            {
                "id": 2,
                "p": "b",
                "s": "a",
                "side": "L",
                "ot": "L",
                "pd": "a",
                "sm": "a",
                "sr": "a",
                "sl": "a",
                "sc": "a",
                "sv": "a",
                "rfo": "a",
                "rfs": "a",
                "status": "EC",
            }
        ]
        self.order_book_runner.update_unmatched(unmatched_orders)
        self.assertEqual(self.order_book_runner.unmatched_orders[1].status, "E")
        self.assertEqual(self.order_book_runner.unmatched_orders[2].status, "EC")
        self.assertEqual(
            self.order_book_runner.unmatched_orders[2].serialised,
            {
                "averagePriceMatched": 0.0,
                "betId": 2,
                "bspLiability": None,
                "cancelledDate": None,
                "customerOrderRef": "a",
                "customerStrategyRef": "a",
                "handicap": 0,
                "lapseStatusReasonCode": None,
                "lapsedDate": None,
                "marketId": "1.123",
                "matchedDate": None,
                "orderType": "LIMIT",
                "persistenceType": None,
                "placedDate": None,
                "priceSize": {"price": "b", "size": "a"},
                "regulatorAuthCode": None,
                "regulatorCode": None,
                "selectionId": 1,
                "side": "LAY",
                "sizeCancelled": "a",
                "sizeLapsed": "a",
                "sizeMatched": "a",
                "sizeRemaining": "a",
                "sizeVoided": "a",
                "status": "EXECUTION_COMPLETE",
            },
        )

    def test_serialise_orders(self):
        mock_order = mock.Mock()
        mock_order.id = 123
        mock_order_two = mock.Mock()
        mock_order_two.id = 456

        unmatched_orders = {
            mock_order.id: mock_order,
            mock_order_two.id: mock_order_two,
        }
        self.order_book_runner.unmatched_orders = unmatched_orders

        def mock_serialise(*args, **kwargs):
            unmatched_orders[789] = "SYM"
            return

        mock_order_two.serialise = mock_serialise

        assert len(self.order_book_runner.serialise_orders()), 2

    def test_serialise_matches(self):
        self.assertEqual(
            self.order_book_runner.serialise_matches(),
            {"matchedBacks": [], "matchedLays": [], "selectionId": 1},
        )


class TestUnmatchedOrder(unittest.TestCase):
    def setUp(self):
        order = {
            "id": 1,
            "p": 2,
            "s": 3,
            "side": "L",
            "status": "E",
            "pt": "L",
            "ot": "L",
            "pd": 8,
            "sm": 9,
            "sr": 10,
            "sl": 11,
            "sc": 12,
            "sv": 13,
            "rfo": 14,
            "rfs": 15,
            "ld": 16,
            "lsrc": 17,
            "error": "test",
            "md": 4,
            "cd": 18,
        }
        self.unmatched_order = UnmatchedOrder(**order)

    def test_init(self):
        assert self.unmatched_order.bet_id == 1
        assert self.unmatched_order.price == 2
        assert self.unmatched_order.size == 3
        assert self.unmatched_order.side == "L"
        assert self.unmatched_order.status == "E"
        assert self.unmatched_order.persistence_type == "L"
        assert self.unmatched_order.order_type == "L"
        assert self.unmatched_order.placed_date == BaseResource.strip_datetime(8)
        assert self.unmatched_order.size_matched == 9
        assert self.unmatched_order.size_remaining == 10
        assert self.unmatched_order.size_lapsed == 11
        assert self.unmatched_order.size_cancelled == 12
        assert self.unmatched_order.size_voided == 13
        assert self.unmatched_order.reference_order == 14
        assert self.unmatched_order.reference_strategy == 15
        assert self.unmatched_order.lapsed_date == BaseResource.strip_datetime(16)
        assert self.unmatched_order.lapse_status_reason_code == 17
        assert self.unmatched_order.cancelled_date == BaseResource.strip_datetime(18)
        assert self.unmatched_order.serialised == {}

    def test_serialise(self):
        self.unmatched_order.serialise("1.23", 12345, 0)
        self.assertEqual(
            self.unmatched_order.serialised,
            {
                "sizeLapsed": 11,
                "persistenceType": "LAPSE",
                "sizeRemaining": 10,
                "placedDate": "1970-01-01T00:00:00.008000Z",
                "sizeVoided": 13,
                "sizeCancelled": 12,
                "betId": 1,
                "customerOrderRef": 14,
                "orderType": "LIMIT",
                "marketId": "1.23",
                "side": "LAY",
                "selectionId": 12345,
                "bspLiability": None,
                "sizeMatched": 9,
                "handicap": 0.0,
                "averagePriceMatched": 0.0,
                "status": "EXECUTABLE",
                "customerStrategyRef": 15,
                "regulatorCode": None,
                "regulatorAuthCode": None,
                "priceSize": {"price": 2, "size": 3},
                "matchedDate": "1970-01-01T00:00:00.004000Z",
                "lapsedDate": "1970-01-01T00:00:00.016000Z",
                "lapseStatusReasonCode": 17,
                "cancelledDate": "1970-01-01T00:00:00.018000Z",
            },
        )


class TestRaceCache(unittest.TestCase):
    def setUp(self):
        self.market_id = "1.12"
        self.publish_time = 123
        self.race_id = "456"
        self.race_cache = RaceCache(
            self.market_id, self.publish_time, self.race_id, True
        )

    def test_init(self):
        self.assertEqual(self.race_cache.market_id, self.market_id)
        self.assertEqual(self.race_cache.publish_time, self.publish_time)
        self.assertEqual(self.race_cache.race_id, self.race_id)
        self.assertTrue(self.race_cache.lightweight)
        self.assertIsNone(self.race_cache.rpc)
        self.assertEqual(self.race_cache.rrc, {})
        self.assertIsNone(self.race_cache.streaming_update)

    def test_update_rpm(self):
        update = {"rpc": 1234}
        publish_time = 1518626764
        self.race_cache.update_cache(update, publish_time)

        assert self.race_cache._datetime_updated is not None
        assert self.race_cache.publish_time == publish_time
        assert self.race_cache.rpc == 1234

    def test_update_rrc(self):
        update = {"rrc": [{"id": 1}]}
        publish_time = 1518626764
        self.race_cache.update_cache(update, publish_time)

        assert self.race_cache._datetime_updated is not None
        assert self.race_cache.publish_time == publish_time
        assert self.race_cache.rrc == {1: {"id": 1}}

    @mock.patch("betfairlightweight.streaming.cache.RaceCache.serialise")
    def test_create_resource_lightweight(self, mock_serialise):
        assert self.race_cache.create_resource(12, True) == mock_serialise

    # @mock.patch('betfairlightweight.streaming.cache.Race')
    # @mock.patch('betfairlightweight.streaming.cache.RaceCache.serialise')
    # def test_create_resource(self, mock_serialise, mock_race):
    #     # print(self.race_cache.create_resource(12, {}, False))
    #     self.assertIsInstance(self.race_cache.create_resource(12, {}, False), mock_race)

    def test_serialise(self):
        self.race_cache.rpc = {"test": 123}
        self.race_cache.rrc = {1: {"test": "me"}}
        self.race_cache.publish_time = 12
        assert self.race_cache.serialise == {
            "pt": 12,
            "mid": self.market_id,
            "id": self.race_id,
            "rpc": {"test": 123},
            "rrc": [{"test": "me"}],
            "streaming_update": None,
        }
