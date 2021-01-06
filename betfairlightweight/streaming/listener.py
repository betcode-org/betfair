import logging
import queue
from typing import Optional

from .stream import BaseStream, MarketStream, OrderStream, RaceStream
from ..compat import json

logger = logging.getLogger(__name__)


class BaseListener:
    def __init__(self, max_latency: Optional[float] = 0.5):
        self.max_latency = max_latency

        self.connection_id = None
        self.status = None
        self.stream = None
        self.stream_type = None  # marketSubscription/orderSubscription/raceSubscription
        self.stream_unique_id = None
        self.connections_available = None  # connection throttling

    def register_stream(self, unique_id: int, operation: str) -> None:
        logger.info("[Register: %s]: %s" % (unique_id, operation))
        if self.stream is not None:
            logger.warning(
                "[Listener: %s]: stream already registered, replacing data" % unique_id
            )
        self.stream_unique_id = unique_id
        self.stream_type = operation
        self.stream = self._add_stream(unique_id, operation)

    def update_unique_id(self, unique_id: int) -> None:
        logger.info(
            "[Register: %s]: Unique id updated on listener and stream" % unique_id
        )
        self.stream_unique_id = unique_id
        self.stream.unique_id = unique_id

    def on_data(self, raw_data: str) -> None:
        logger.info(raw_data)

    def snap(self, market_ids: list = None) -> list:
        """Returns a 'snap' of the current cache
        data.

        :param list market_ids: Market ids to return
        :return: Return List of resources
        """
        if self.stream_type:  # quicker than self.stream due to __len__ call
            return self.stream.snap(market_ids)
        else:
            return []

    @property
    def updates_processed(self) -> int:
        if self.stream:
            return self.stream._updates_processed

    @property
    def initial_clk(self) -> str:
        if self.stream is not None:
            return self.stream._initial_clk

    @property
    def clk(self) -> str:
        if self.stream is not None:
            return self.stream._clk

    def _add_stream(self, unique_id: int, operation: str) -> BaseStream:
        if operation == "marketSubscription":
            return MarketStream(self, unique_id)
        elif operation == "orderSubscription":
            return OrderStream(self, unique_id)
        elif operation == "raceSubscription":
            return RaceStream(self, unique_id)

    def __str__(self) -> str:
        return "{0}".format(self.__class__.__name__)

    def __repr__(self) -> str:
        return "<{0}>".format(self.__class__.__name__)


class StreamListener(BaseListener):
    """Stream listener, processes results from socket,
    holds a stream which can hold order or market book
    caches
    """

    def __init__(
        self,
        output_queue: queue.Queue = None,
        max_latency: Optional[float] = 0.5,
        lightweight: bool = False,
        debug: bool = True,
        update_clk: bool = True,
    ):
        """
        :param Queue output_queue: Queue used to return data
        :param float max_latency: Logs warning if latency above value
        :param bool lightweight: Returns dict instead of resource
        :param bool debug: Debug logging calls enabled (setting to True has slight performance hit)
        :param bool update_clk: initialClk/clk not updated on updates if False (quicker)
        """
        super(StreamListener, self).__init__(max_latency)
        self.output_queue = output_queue
        self.lightweight = lightweight
        self.debug = debug
        self.update_clk = update_clk

    def on_data(self, raw_data: str) -> Optional[bool]:
        """Called when raw data is received from connection.
        Override this method if you wish to manually handle
        the stream data

        :param raw_data: Received raw data
        :return: Return False to stop stream and close connection
        """
        try:
            data = json.loads(raw_data)
        except ValueError:
            logger.error("value error: %s" % raw_data)
            return

        self.status = data.get("status")
        unique_id = data.get("id")

        if self._error_handler(data, unique_id):
            return False

        operation = data["op"]
        if operation == "connection":
            self._on_connection(data, unique_id)
        elif operation == "status":
            self._on_status(data, unique_id)
        elif operation in ["mcm", "ocm", "rcm"]:
            # historic data does not contain unique_id
            if self.stream_unique_id not in [unique_id, 0]:
                logger.warning(
                    "Unwanted data received from uniqueId: %s, expecting: %s"
                    % (unique_id, self.stream_unique_id)
                )
                return
            self._on_change_message(data, unique_id)

    def _on_connection(self, data: dict, unique_id: int) -> None:
        """Called on collection operation

        :param data: Received data
        """
        if unique_id is None:
            unique_id = self.stream_unique_id
        self.connection_id = data.get("connectionId")
        logger.info(
            "[%s: %s]: connection_id: %s" % (self.stream, unique_id, self.connection_id)
        )

    def _on_status(self, data: dict, unique_id: int) -> None:
        """Called on status operation

        :param data: Received data
        """
        status_code = data.get("statusCode")
        connections_available = data.get("connectionsAvailable")
        if connections_available:
            self.connections_available = data.get("connectionsAvailable")
        logger.info(
            "[%s: %s]: %s (%s connections available)"
            % (self.stream, unique_id, status_code, self.connections_available)
        )

    def _on_change_message(self, data: dict, unique_id: int) -> None:
        change_type = data.get("ct", "UPDATE")

        if self.debug:
            logger.debug(  # very slow call due to data dict
                "[%s: %s]: %s: %s" % (self.stream, unique_id, change_type, data)
            )

        if change_type == "SUB_IMAGE":
            self.stream.on_subscribe(data)
        elif change_type == "RESUB_DELTA":
            self.stream.on_resubscribe(data)
        elif change_type == "HEARTBEAT":
            self.stream.on_heartbeat(data)
        elif change_type == "UPDATE":
            self.stream.on_update(data)

    def _error_handler(self, data: dict, unique_id: int) -> Optional[bool]:
        """Called when data first received

        :param data: Received data
        :param unique_id: Unique id
        :return: True if error present
        """
        if data.get("statusCode") == "FAILURE":
            logger.error(
                "[%s: %s]: %s: %s"
                % (
                    self.stream,
                    unique_id,
                    data.get("errorCode"),
                    data.get("errorMessage"),
                )
            )
            if data.get("connectionClosed"):
                return True
        if self.status:
            # Clients shouldn't disconnect if status 503 is returned; when the stream
            # recovers updates will be sent containing the latest data
            logger.warning(
                "[%s: %s]: status: %s" % (self.stream, unique_id, self.status)
            )
