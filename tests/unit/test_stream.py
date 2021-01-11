import unittest
from unittest import mock

from betfairlightweight.streaming.stream import (
    BaseStream,
    MarketStream,
    OrderStream,
    RaceStream,
    MAX_CACHE_AGE,
)
from tests.unit.tools import create_mock_json


class BaseStreamTest(unittest.TestCase):
    def setUp(self):
        self.listener = mock.Mock()
        self.listener.max_latency = 0.5
        self.stream = BaseStream(self.listener, 123)

    def test_init(self):
        assert self.stream._listener == self.listener
        assert self.stream.unique_id == 123
        assert self.stream.output_queue == self.listener.output_queue
        assert self.stream.update_clk == self.listener.update_clk
        assert self.stream._max_latency == self.listener.max_latency
        assert self.stream._lightweight == self.listener.lightweight
        assert self.stream._initial_clk is None
        assert self.stream._clk is None
        assert self.stream._caches == {}
        assert self.stream._updates_processed == 0
        assert self.stream.time_created is not None
        assert self.stream.time_updated is not None
        assert self.stream._lookup == "mc"
        assert self.stream._name == "Stream"
        assert MAX_CACHE_AGE == 60 * 60 * 8

    @mock.patch("betfairlightweight.streaming.stream.BaseStream._process")
    @mock.patch("betfairlightweight.streaming.stream.BaseStream._update_clk")
    def test_on_subscribe(self, mock_update_clk, mock_process):
        self.stream.on_subscribe({})
        mock_update_clk.assert_called_once_with({})

        self.stream.on_subscribe({"mc": {123}})
        mock_process.assert_called_once_with({123}, None)

    @mock.patch("betfairlightweight.streaming.stream.BaseStream._update_clk")
    def test_on_heartbeat(self, mock_update_clk):
        self.stream.on_heartbeat({})
        mock_update_clk.assert_called_once_with({})

    @mock.patch("betfairlightweight.streaming.stream.BaseStream.on_update")
    def test_on_resubscribe(self, mock_on_update):
        self.stream.on_resubscribe({})
        mock_on_update.assert_called_once_with({})

    @mock.patch("betfairlightweight.streaming.stream.BaseStream.clear_stale_cache")
    @mock.patch(
        "betfairlightweight.streaming.stream.BaseStream._process", return_value=False
    )
    @mock.patch(
        "betfairlightweight.streaming.stream.BaseStream._calc_latency", return_value=0.1
    )
    @mock.patch("betfairlightweight.streaming.stream.BaseStream._update_clk")
    def test_on_update(
        self, mock_update_clk, mock_calc_latency, mock_process, mock_clear_stale_cache
    ):
        mock_response = create_mock_json("tests/resources/streaming_mcm_update.json")
        self.stream.on_update(mock_response.json())

        mock_update_clk.assert_called_with(mock_response.json())
        mock_calc_latency.assert_called_with(mock_response.json().get("pt"))
        mock_process.assert_called_with(
            mock_response.json().get("mc"), mock_response.json().get("pt")
        )

        mock_calc_latency.return_value = 10
        self.stream.on_update(mock_response.json())
        mock_clear_stale_cache.assert_not_called()

    @mock.patch("betfairlightweight.streaming.stream.BaseStream.clear_stale_cache")
    @mock.patch(
        "betfairlightweight.streaming.stream.BaseStream._process", return_value=True
    )
    @mock.patch(
        "betfairlightweight.streaming.stream.BaseStream._calc_latency", return_value=0.1
    )
    @mock.patch("betfairlightweight.streaming.stream.BaseStream._update_clk")
    def test_on_update_clear_cache(
        self, mock_update_clk, mock_calc_latency, mock_process, mock_clear_stale_cache
    ):
        mock_response = create_mock_json("tests/resources/streaming_mcm_update.json")
        self.stream.on_update(mock_response.json())

        mock_update_clk.assert_called_with(mock_response.json())
        mock_calc_latency.assert_called_with(mock_response.json().get("pt"))
        mock_process.assert_called_with(
            mock_response.json().get("mc"), mock_response.json().get("pt")
        )

        mock_calc_latency.return_value = 10
        self.stream.on_update(mock_response.json())
        mock_clear_stale_cache.assert_called_with(mock_response.json().get("pt"))

    @mock.patch("betfairlightweight.streaming.stream.BaseStream._process")
    @mock.patch(
        "betfairlightweight.streaming.stream.BaseStream._calc_latency", return_value=0.1
    )
    @mock.patch("betfairlightweight.streaming.stream.BaseStream._update_clk")
    def test_on_update_no_latency(
        self, mock_update_clk, mock_calc_latency, mock_process
    ):
        data = {"pt": 12345, "mc": "trainer"}
        self.listener.max_latency = None
        self.stream.on_update(data)

        mock_update_clk.assert_called_with(data)
        mock_calc_latency.assert_called_with(data.get("pt"))
        mock_process.assert_called_with(data.get("mc"), data.get("pt"))

    def test_clear_cache(self):
        self.stream._caches = {1: "abc"}
        self.stream.clear_cache()

        assert self.stream._caches == {}

    def test_clear_stale_cache(self):
        market_a = mock.Mock(market_id="1.23", publish_time=123, closed=False)
        market_b = mock.Mock(market_id="4.56", publish_time=123, closed=True)
        self.stream._caches = {
            "1.23": market_a,
            "4.56": market_b,
        }
        self.stream.clear_stale_cache(123456789)
        self.assertEqual(self.stream._caches, {"1.23": market_a})

    def test_snap(self):
        market_books = self.stream.snap()
        assert market_books == []

        mock_cache = mock.Mock()
        mock_cache.market_id = "1.1"
        self.stream._caches = {"1.1": mock_cache}

        market_books = self.stream.snap()
        mock_cache.create_resource.assert_called_with(self.stream.unique_id, snap=True)
        assert market_books == [mock_cache.create_resource()]

        market_books = self.stream.snap(["1.2"])
        assert market_books == []

        market_books = self.stream.snap(["1.1"])
        assert market_books == [mock_cache.create_resource()]

    def test_snap_dict_size_err(self):
        mock_cache = mock.Mock()
        mock_cache.market_id = "1.1"

        def _change_dict(*_, **__):
            self.stream._caches["1.{}".format(len(self.stream._caches))] = mock_cache

        mock_cache.create_resource = _change_dict
        self.stream._caches = {"1.{}".format(i): mock_cache for i in range(2)}

        self.stream.snap()

    def test_on_creation(self):
        self.stream._on_creation()

    def test_process(self):
        self.stream._process(None, None)

    def test_on_process(self):
        mock_cache_one = mock.Mock()
        mock_cache_two = mock.Mock()
        self.stream.on_process([mock_cache_one, mock_cache_two])
        self.stream.output_queue.put.assert_called_with(
            [mock_cache_one.create_resource(), mock_cache_two.create_resource()]
        )

    def test_update_clk(self):
        self.stream._update_clk({"initialClk": 1234})
        assert self.stream._initial_clk == 1234

        self.stream._update_clk({"clk": 123})
        assert self.stream._clk == 123

    @mock.patch("time.time", return_value=1485554805.107185)
    def test_calc_latency(self, mock_time):
        pt = 1485554796455
        assert self.stream._calc_latency(pt) is not None
        assert abs(self.stream._calc_latency(pt) - 8.652184) < 1e-5

    def test_len(self):
        assert len(self.stream) == 0

    def test_str(self):
        assert str(self.stream) == "Stream"

    def test_repr(self):
        assert repr(self.stream) == "<Stream [0]>"


class MarketStreamTest(unittest.TestCase):
    def setUp(self):
        self.listener = mock.Mock()
        self.stream = MarketStream(self.listener, 123)

    def test_init(self):
        assert self.stream._lookup == "mc"
        assert self.stream._name == "MarketStream"

    @mock.patch("betfairlightweight.streaming.stream.MarketStream._process")
    @mock.patch("betfairlightweight.streaming.stream.MarketStream._update_clk")
    def test_on_subscribe(self, mock_update_clk, mock_process):
        self.stream.on_subscribe({})
        mock_update_clk.assert_called_once_with({})
        self.stream.on_subscribe({"mc": {123}})
        mock_process.assert_called_once_with({123}, None)

    @mock.patch("betfairlightweight.streaming.stream.MarketBookCache")
    @mock.patch("betfairlightweight.streaming.stream.MarketStream.on_process")
    def test_process(self, mock_on_process, mock_cache):
        sub_image = create_mock_json("tests/resources/streaming_mcm_SUB_IMAGE.json")
        data = sub_image.json()["mc"]
        self.assertTrue(self.stream._process(data, 123))
        self.assertEqual(len(self.stream), len(data))
        mock_on_process.assert_called_with([mock_cache()])

    @mock.patch("betfairlightweight.streaming.stream.MarketBookCache")
    @mock.patch("betfairlightweight.streaming.stream.MarketStream.on_process")
    def test_process_no_market_definition(self, mock_on_process, mock_cache):
        sub_image_error = create_mock_json(
            "tests/resources/streaming_mcm_SUB_IMAGE_no_market_def.json"
        )
        data = sub_image_error.json()["mc"]
        self.assertTrue(self.stream._process(data, 123))
        self.assertEqual(len(data), 137)
        self.assertEqual(len(self.stream), 137)  # two markets not missing

    @mock.patch("betfairlightweight.streaming.stream.MarketBookCache")
    @mock.patch("betfairlightweight.streaming.stream.MarketStream.on_process")
    def test_process_no_img(self, mock_on_process, mock_cache):
        sub_image = create_mock_json("tests/resources/streaming_mcm_SUB_IMAGE.json")
        data = sub_image.json()["mc"]
        data[0]["img"] = False
        mock_market_cache = mock_cache()
        self.stream._caches = {data[0]["id"]: mock_market_cache}
        self.assertFalse(self.stream._process(data, 123))
        self.assertEqual(len(self.stream), len(data))
        mock_market_cache.update_cache.assert_called_with(data[0], 123)

    def test_str(self):
        assert str(self.stream) == "MarketStream"

    def test_repr(self):
        assert repr(self.stream) == "<MarketStream [0]>"


class OrderStreamTest(unittest.TestCase):
    def setUp(self):
        self.listener = mock.Mock()
        self.stream = OrderStream(self.listener, 123)

    def test_init(self):
        assert self.stream._lookup == "oc"
        assert self.stream._name == "OrderStream"

    @mock.patch("betfairlightweight.streaming.stream.OrderStream._process")
    @mock.patch("betfairlightweight.streaming.stream.OrderStream._update_clk")
    def test_on_subscribe(self, mock_update_clk, mock_process):
        self.stream.on_subscribe({})
        mock_update_clk.assert_called_once_with({})
        self.stream.on_subscribe({"oc": {123}})
        mock_process.assert_called_once_with({123}, None)

    @mock.patch("betfairlightweight.streaming.stream.OrderBookCache")
    @mock.patch("betfairlightweight.streaming.stream.OrderStream.on_process")
    def test_process(self, mock_on_process, mock_cache):
        sub_image = create_mock_json("tests/resources/streaming_ocm_FULL_IMAGE.json")
        data = sub_image.json()["oc"]
        self.assertTrue(self.stream._process(data, 123))
        self.assertEqual(len(self.stream), len(data))
        self.assertFalse(self.stream._process(data, 123))
        mock_on_process.assert_called_with([mock_cache()])

    @mock.patch("betfairlightweight.streaming.stream.OrderBookCache")
    @mock.patch("betfairlightweight.streaming.stream.OrderStream.on_process")
    def test_process_new_image(self, mock_on_process, mock_cache):
        self.stream._caches = {"1.161613698": mock.Mock()}
        sub_image = create_mock_json(
            "tests/resources/streaming_ocm_NEW_FULL_IMAGE.json"
        )
        data = sub_image.json()["oc"]
        self.assertTrue(self.stream._process(data, 123))
        self.assertEqual(len(self.stream), len(data))
        self.assertTrue(self.stream._process(data, 123))

    @mock.patch("betfairlightweight.streaming.stream.OrderBookCache")
    @mock.patch("betfairlightweight.streaming.stream.OrderStream.on_process")
    def test_process_empty_image(self, mock_on_process, mock_cache):
        self.stream._caches = {"1.161613698": mock.Mock()}
        sub_image = create_mock_json("tests/resources/streaming_ocm_EMPTY_IMAGE.json")
        data = sub_image.json()["oc"]
        self.assertTrue(self.stream._process(data, 123))
        self.assertEqual(len(self.stream), len(data))
        self.assertTrue(self.stream._process(data, 123))

    def test_str(self):
        assert str(self.stream) == "OrderStream"

    def test_repr(self):
        assert repr(self.stream) == "<OrderStream [0]>"


class RaceStreamTest(unittest.TestCase):
    def setUp(self):
        self.listener = mock.Mock()
        self.stream = RaceStream(self.listener, 123)

    def test_init(self):
        assert self.stream._lookup == "rc"
        assert self.stream._name == "RaceStream"

    @mock.patch("betfairlightweight.streaming.stream.RaceCache")
    @mock.patch("betfairlightweight.streaming.stream.RaceStream.on_process")
    def test_process(self, mock_on_process, mock_race_cache):
        update = [{"mid": "1.234567", "yad": "a"}]
        publish_time = 1234
        self.assertFalse(self.stream._process(update, publish_time))
        assert self.stream._caches["1.234567"] == mock_race_cache()
        mock_race_cache().update_cache.assert_called_with(update[0], publish_time)
        mock_on_process.assert_called_with([mock_race_cache()])

    def test_str(self):
        assert str(self.stream) == "RaceStream"

    def test_repr(self):
        assert repr(self.stream) == "<RaceStream [0]>"
