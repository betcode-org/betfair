import unittest
from unittest import mock

from betfairlightweight.streaming.listener import BaseListener, StreamListener
from tests.unit.tools import create_mock_json


class BaseListenerTest(unittest.TestCase):
    def setUp(self):
        self.base_listener = BaseListener()

    def test_init(self):
        assert self.base_listener.connection_id is None
        assert self.base_listener.status is None
        assert self.base_listener.stream is None
        assert self.base_listener.stream_unique_id is None
        assert self.base_listener.stream_type is None
        assert self.base_listener.max_latency == 0.5
        assert self.base_listener.connections_available is None

    @mock.patch(
        "betfairlightweight.streaming.listener.BaseListener._add_stream",
        return_value=123,
    )
    def test_register_stream(self, mock_add_stream):
        self.base_listener.register_stream(1, "authentication")

        self.base_listener.register_stream(2, "marketSubscription")
        mock_add_stream.assert_called_with(2, "marketSubscription")
        assert self.base_listener.stream == 123

        self.base_listener.market_stream = "test"
        self.base_listener.register_stream(2, "marketSubscription")
        mock_add_stream.assert_called_with(2, "marketSubscription")
        assert self.base_listener.stream == 123

        self.base_listener.register_stream(3, "orderSubscription")
        mock_add_stream.assert_called_with(3, "orderSubscription")
        assert self.base_listener.stream == 123

        self.base_listener.order_stream = "test"
        self.base_listener.register_stream(3, "orderSubscription")
        mock_add_stream.assert_called_with(3, "orderSubscription")
        assert self.base_listener.stream == 123

        self.base_listener.register_stream(2, "raceSubscription")
        mock_add_stream.assert_called_with(2, "raceSubscription")
        assert self.base_listener.stream == 123

        self.base_listener.register_stream(2, "raceSubscription")
        mock_add_stream.assert_called_with(2, "raceSubscription")
        assert self.base_listener.stream == 123

    def test_update_unique_id(self):
        self.base_listener.stream = mock.Mock()
        self.base_listener.update_unique_id(987)
        self.assertEqual(self.base_listener.stream_unique_id, 987)
        self.assertEqual(self.base_listener.stream.unique_id, 987)

    def test_on_data(self):
        self.base_listener.on_data({})

    @mock.patch("betfairlightweight.streaming.listener.RaceStream", return_value=789)
    @mock.patch("betfairlightweight.streaming.listener.OrderStream", return_value=456)
    @mock.patch("betfairlightweight.streaming.listener.MarketStream", return_value=123)
    def test_add_stream(self, mock_market_stream, mock_order_stream, mock_race_stream):
        new_stream = self.base_listener._add_stream(1, "marketSubscription")
        assert new_stream == 123
        mock_market_stream.assert_called_with(self.base_listener, 1)

        new_stream = self.base_listener._add_stream(1, "orderSubscription")
        assert new_stream == 456
        mock_order_stream.assert_called_with(self.base_listener, 1)

        new_stream = self.base_listener._add_stream(1, "raceSubscription")
        assert new_stream == 789
        mock_race_stream.assert_called_with(self.base_listener, 1)

    def test_snap(self):
        mock_stream = mock.Mock()
        self.base_listener.stream = mock_stream
        self.base_listener.stream_type = None
        assert self.base_listener.snap() == []

        self.base_listener.stream_type = "test"
        assert self.base_listener.snap() == mock_stream.snap(None)

    def test_props(self):
        assert self.base_listener.initial_clk is None
        assert self.base_listener.clk is None
        stream = mock.Mock()
        stream._initial_clk = 2
        stream._clk = 1
        self.base_listener.stream = stream
        assert self.base_listener.initial_clk == 2
        assert self.base_listener.clk == 1

    def test_updates_processed(self):
        assert self.base_listener.updates_processed is None

        mock_stream = mock.Mock()
        mock_stream._updates_processed = 100
        self.base_listener.stream = mock_stream
        assert self.base_listener.updates_processed == 100

    def test_str(self):
        assert str(self.base_listener) == "BaseListener"

    def test_repr(self):
        assert repr(self.base_listener) == "<BaseListener>"


class StreamListenerTest(unittest.TestCase):
    def setUp(self):
        self.output_queue = mock.Mock()
        self.max_latency = 10.0
        self.stream_listener = StreamListener(self.output_queue, self.max_latency)

    def test_init(self):
        assert self.stream_listener.output_queue == self.output_queue
        assert self.stream_listener.max_latency == self.max_latency
        assert self.stream_listener.debug == True

    @mock.patch("betfairlightweight.streaming.listener.StreamListener._on_connection")
    @mock.patch("betfairlightweight.streaming.listener.StreamListener._on_status")
    @mock.patch(
        "betfairlightweight.streaming.listener.StreamListener._on_change_message"
    )
    @mock.patch(
        "betfairlightweight.streaming.listener.StreamListener._error_handler",
        return_value=False,
    )
    def test_on_data(
        self,
        mock_error_handler,
        mock_on_change_message,
        mock_on_status,
        mock_on_connection,
    ):
        self.stream_listener.stream_unique_id = 2

        mock_response = create_mock_json("tests/resources/streaming_connection.json")
        self.stream_listener.on_data(mock_response.text)
        mock_error_handler.assert_called_with(
            mock_response.json(), mock_response.json().get("id")
        )
        mock_on_connection.assert_called_with(
            mock_response.json(), mock_response.json().get("id")
        )

        mock_response = create_mock_json("tests/resources/streaming_status.json")
        self.stream_listener.on_data(mock_response.text)
        mock_error_handler.assert_called_with(
            mock_response.json(), mock_response.json().get("id")
        )
        mock_on_status.assert_called_with(
            mock_response.json(), mock_response.json().get("id")
        )

        mock_response = create_mock_json("tests/resources/streaming_mcm_update.json")
        self.stream_listener.on_data(mock_response.text)
        mock_error_handler.assert_called_with(
            mock_response.json(), mock_response.json().get("id")
        )
        mock_on_change_message.assert_called_with(
            mock_response.json(), mock_response.json().get("id")
        )

        mock_response = create_mock_json("tests/resources/streaming_rcm.json")
        self.stream_listener.on_data(mock_response.text)
        mock_error_handler.assert_called_with(
            mock_response.json(), mock_response.json().get("id")
        )
        mock_on_change_message.assert_called_with(
            mock_response.json(), mock_response.json().get("id")
        )

        mock_response = create_mock_json("tests/resources/streaming_rcm.json")
        self.stream_listener.on_data(mock_response.text)
        mock_error_handler.assert_called_with(
            mock_response.json(), mock_response.json().get("id")
        )
        mock_on_change_message.assert_called_with(
            mock_response.json(), mock_response.json().get("id")
        )

        on_data = self.stream_listener.on_data("some content")
        assert on_data is None

        mock_error_handler.return_value = True
        on_data = self.stream_listener.on_data(mock_response.text)
        assert on_data is False

    @mock.patch(
        "betfairlightweight.streaming.listener.StreamListener._error_handler",
        return_value=True,
    )
    def test_on_data_status_error(
        self,
        mock_error_handler,
    ):
        self.stream_listener.stream_unique_id = 2
        mock_response = create_mock_json("tests/resources/streaming_503.json")
        self.assertFalse(self.stream_listener.on_data(mock_response.text))
        mock_error_handler.assert_called_with(
            mock_response.json(), mock_response.json().get("id")
        )
        self.assertEqual(self.stream_listener.status, 503)

    def test_on_connection(self):
        self.stream_listener._on_connection({"connectionId": 1234}, 1)
        assert self.stream_listener.connection_id == 1234

    def test_on_status(self):
        self.stream_listener._on_status({}, 1)
        self.assertIsNone(self.stream_listener.connections_available)
        self.stream_listener._on_status({"connectionsAvailable": 69}, 1)
        self.assertEqual(self.stream_listener.connections_available, 69)

    def test_on_change_message(self):
        stream = mock.Mock()
        self.stream_listener.stream = stream

        mock_response = create_mock_json("tests/resources/streaming_mcm_SUB_IMAGE.json")
        self.stream_listener._on_change_message(mock_response.json(), 1)
        stream.on_subscribe.assert_called_with(mock_response.json())

        mock_response = create_mock_json(
            "tests/resources/streaming_mcm_RESUB_DELTA.json"
        )
        self.stream_listener._on_change_message(mock_response.json(), 1)
        stream.on_resubscribe.assert_called_with(mock_response.json())

        mock_response = create_mock_json("tests/resources/streaming_mcm_HEARTBEAT.json")
        self.stream_listener._on_change_message(mock_response.json(), 1)
        stream.on_heartbeat.assert_called_with(mock_response.json())

        mock_response = create_mock_json("tests/resources/streaming_mcm_update.json")
        self.stream_listener._on_change_message(mock_response.json(), 1)
        stream.on_update.assert_called_with(mock_response.json())

        mock_response = create_mock_json("tests/resources/streaming_ocm_SUB_IMAGE.json")
        self.stream_listener._on_change_message(mock_response.json(), 1)
        stream.on_subscribe.assert_called_with(mock_response.json())

        # race
        mock_response = create_mock_json("tests/resources/streaming_rcm.json")
        self.stream_listener._on_change_message(mock_response.json(), 1)
        stream.on_update.assert_called_with(mock_response.json())

    def test_error_handler(self):
        mock_response = create_mock_json("tests/resources/streaming_connection.json")
        self.stream_listener._error_handler(mock_response.json(), 1)

        error_data = {
            "errorMessage": "AppKey is not valid",
            "connectionClosed": True,
            "connectionId": "005-015616813698-533678",
            "op": "status",
            "id": 2,
            "errorCode": "INVALID_APP_KEY",
            "statusCode": "FAILURE",
        }
        return_value = self.stream_listener._error_handler(error_data, 1)
        assert return_value is True

        error_data = {
            "errorMessage": "Customer tried to subscribe to more markets than allowed to",
            "connectionClosed": False,
            "connectionId": "005-015616813698-533678",
            "op": "status",
            "id": 2,
            "errorCode": "SUBSCRIPTION_LIMIT_EXCEEDED",
            "statusCode": "FAILURE",
        }
        return_value = self.stream_listener._error_handler(error_data, 1)
        assert return_value is None

    def test_error_handler_503(self):
        self.stream_listener.status = "503"
        mock_response = create_mock_json("tests/resources/streaming_connection.json")
        self.stream_listener._error_handler(mock_response.json(), 1)

    def test_str(self):
        assert str(self.stream_listener) == "StreamListener"

    def test_repr(self):
        assert repr(self.stream_listener) == "<StreamListener>"
