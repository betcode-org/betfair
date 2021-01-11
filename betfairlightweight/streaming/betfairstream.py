import socket
import ssl
import logging
import datetime
import collections
from typing import Optional

from ..exceptions import SocketError, ListenerError
from ..compat import json
from .listener import BaseListener

logger = logging.getLogger(__name__)


class BetfairStream:
    """Socket holder, connects to betfair and
    pushes any received data to listener
    """

    __port = 443
    __CRLF = "\r\n"
    __encoding = "utf-8"

    HOSTS = collections.defaultdict(
        lambda: "stream-api.betfair.com",
        integration="stream-api-integration.betfair.com",
        race="sports-data-stream-api.betfair.com",
    )

    def __init__(
        self,
        unique_id: int,
        listener: BaseListener,
        app_key: str,
        session_token: str,
        timeout: float,
        buffer_size: int,
        host: Optional[str],
    ):
        self._unique_id = unique_id
        self.listener = listener
        self.app_key = app_key
        self.session_token = session_token
        self.timeout = timeout
        self.buffer_size = buffer_size
        self.host = self.HOSTS[host]
        self.receive_count = 0
        self.datetime_last_received = None

        self._socket = None
        self._running = False

    def start(self) -> None:
        """Starts read loop, connects/authenticates
        if not already running.
        """
        if not self._running:
            self._connect()
            self.authenticate()
        self._read_loop()

    def stop(self) -> None:
        """Stops read loop and closes socket if it has been created."""
        self._running = False

        if self._socket is None:
            return
        try:
            self._socket.shutdown(socket.SHUT_RDWR)
            self._socket.close()
        except socket.error:
            pass
        self._socket = None

    def authenticate(self) -> int:
        """Authentication request."""
        unique_id = self.new_unique_id()
        message = {
            "op": "authentication",
            "id": unique_id,
            "appKey": self.app_key,
            "session": self.session_token,
        }
        self._send(message)
        return unique_id

    def heartbeat(self) -> int:
        """Heartbeat request to keep session alive."""
        unique_id = self.new_unique_id()
        message = {"op": "heartbeat", "id": unique_id}
        self._send(message)
        return unique_id

    def subscribe_to_markets(
        self,
        market_filter: dict,
        market_data_filter: dict,
        initial_clk: str = None,
        clk: str = None,
        conflate_ms: int = None,
        heartbeat_ms: int = None,
        segmentation_enabled: bool = True,
    ) -> int:
        """
        Market subscription request.

        :param dict market_filter: Market filter
        :param dict market_data_filter: Market data filter
        :param str initial_clk: Sequence token for reconnect
        :param str clk: Sequence token for reconnect
        :param int conflate_ms: conflation rate (bounds are 0 to 120000)
        :param int heartbeat_ms: heartbeat rate (500 to 5000)
        :param bool segmentation_enabled: allow the server to send large sets of data
        in segments, instead of a single block
        """
        unique_id = self.new_unique_id()
        message = {
            "op": "marketSubscription",
            "id": unique_id,
            "marketFilter": market_filter,
            "marketDataFilter": market_data_filter,
            "initialClk": initial_clk,
            "clk": clk,
            "conflateMs": conflate_ms,
            "heartbeatMs": heartbeat_ms,
            "segmentationEnabled": segmentation_enabled,
        }
        if initial_clk and clk:
            # if resubscribe only update unique_id
            self.listener.update_unique_id(unique_id)
        else:
            self.listener.register_stream(unique_id, "marketSubscription")
        self._send(message)
        return unique_id

    def subscribe_to_orders(
        self,
        order_filter: dict = None,
        initial_clk: str = None,
        clk: str = None,
        conflate_ms: int = None,
        heartbeat_ms: int = None,
        segmentation_enabled: bool = True,
    ) -> int:
        """
        Order subscription request.

        :param dict order_filter: Order filter to be applied
        :param str initial_clk: Sequence token for reconnect
        :param str clk: Sequence token for reconnect
        :param int conflate_ms: conflation rate (bounds are 0 to 120000)
        :param int heartbeat_ms: heartbeat rate (500 to 5000)
        :param bool segmentation_enabled: allow the server to send large sets of data
        in segments, instead of a single block
        """
        unique_id = self.new_unique_id()
        message = {
            "op": "orderSubscription",
            "id": unique_id,
            "orderFilter": order_filter,
            "initialClk": initial_clk,
            "clk": clk,
            "conflateMs": conflate_ms,
            "heartbeatMs": heartbeat_ms,
            "segmentationEnabled": segmentation_enabled,
        }
        if initial_clk and clk:
            # if resubscribe only update unique_id
            self.listener.update_unique_id(unique_id)
        else:
            self.listener.register_stream(unique_id, "orderSubscription")
        self._send(message)
        return unique_id

    def subscribe_to_races(self) -> int:
        """Race subscription request."""
        unique_id = self.new_unique_id()
        message = {"op": "raceSubscription", "id": unique_id}
        self.listener.register_stream(unique_id, "raceSubscription")
        self._send(message)
        return unique_id

    def new_unique_id(self) -> int:
        self._unique_id += 1
        return self._unique_id

    def _connect(self) -> None:
        """Creates socket and sets running to True."""
        self._socket = self._create_socket()
        self._running = True

    def _create_socket(self) -> socket.socket:
        """Creates ssl socket, connects to stream api and
        sets timeout.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = ssl.wrap_socket(s)
        s.connect((self.host, self.__port))
        s.settimeout(self.timeout)
        return s

    def _read_loop(self) -> None:
        """Read loop, splits by CRLF and pushes received data
        to _data.
        """
        while self._running:
            received_data_raw = self._receive_all()
            if self._running:
                self.receive_count += 1
                self.datetime_last_received = datetime.datetime.utcnow()
                received_data_split = received_data_raw.split(self.__CRLF)
                for received_data in received_data_split:
                    if received_data:
                        self._data(received_data)

    def _receive_all(self) -> Optional[str]:
        """Whilst socket is running receives data from socket,
        till CRLF is detected.
        """
        (data, part) = ("", "")
        crlf_bytes = bytes(self.__CRLF, encoding=self.__encoding)

        while self._running and part[-2:] != crlf_bytes:
            try:
                part = self._socket.recv(self.buffer_size)
            except (socket.timeout, socket.error) as e:
                if self._running:
                    self.stop()
                    raise SocketError("[Connect: %s]: Socket %s" % (self._unique_id, e))
                else:
                    return  # 133, prevents error if stop is called mid recv

            # an empty string indicates the server shutdown the socket
            if len(part) == 0:
                if self._running:
                    self.stop()
                    raise SocketError(
                        "[Connect: %s]: Connection closed by server"
                        % (self._unique_id,)
                    )
                else:
                    return  # 165, prevents error if stop is called mid recv

            data += part.decode(self.__encoding)
        return data

    def _data(self, received_data: str) -> None:
        """Sends data to listener, if False is returned; socket
        is closed.

        :param received_data: Decoded data received from socket.
        """
        if self.listener.on_data(received_data) is False:
            self.stop()
            raise ListenerError(self.listener.connection_id, received_data)

    def _send(self, message: dict) -> None:
        """If not running connects socket and
        authenticates. Adds CRLF and sends message
        to Betfair.

        :param message: Data to be sent to Betfair.
        """
        if not self._running:
            self._connect()
            self.authenticate()

        message_dumped = json.dumps(message)

        if not isinstance(
            message_dumped, bytes
        ):  # handles orjson as `orjson.dumps -> bytes` but `json.dumps -> str`
            message_dumped = message_dumped.encode(encoding=self.__encoding)
        crlf = bytes(self.__CRLF, encoding=self.__encoding)
        message_dumped += crlf

        logger.debug(
            "[Subscription: %s] Sending: %s" % (self._unique_id, repr(message_dumped))
        )
        try:
            self._socket.sendall(message_dumped)
        except (socket.timeout, socket.error) as e:
            self.stop()
            raise SocketError("[Connect: %s]: Socket %s" % (self._unique_id, e))

    def __str__(self) -> str:
        return "<BetfairStream [%s]>" % ("running" if self._running else "not running")

    def __repr__(self) -> str:
        return "<BetfairStream>"


class HistoricalStream:
    """Copy of 'Betfair Stream' for parsing
    historical data.
    """

    def __init__(
        self, file_path: str, listener: BaseListener, operation: str, unique_id: int
    ):
        """
        :param str file_path: Directory of betfair data
        :param BaseListener listener: Listener object
        :param str operation: Operation type
        :param int unique_id: Stream id (added to updates)
        """
        self.file_path = file_path
        self.listener = listener
        self.operation = operation
        self.unique_id = unique_id
        self._running = False

    def start(self) -> None:
        self._running = True
        self._read_loop()

    def stop(self) -> None:
        self._running = False

    def _read_loop(self) -> None:
        self.listener.register_stream(self.unique_id, self.operation)
        with open(self.file_path, "r") as f:
            for update in f:
                if self.listener.on_data(update) is False:
                    # if on_data returns an error stop the stream and raise error
                    self.stop()
                    raise ListenerError("HISTORICAL", update)
                if not self._running:
                    break
            else:
                # if f has finished, also stop the stream
                self.stop()


class HistoricalGeneratorStream(HistoricalStream):
    """Copy of 'Betfair Stream' for parsing
    historical data (no threads).
    """

    def get_generator(self):
        return self._read_loop

    def _read_loop(self) -> dict:
        self._running = True
        self.listener.register_stream(self.unique_id, self.operation)
        with open(self.file_path, "r") as f:
            for update in f:
                if self.listener.on_data(update) is False:
                    # if on_data returns an error stop the stream and raise error
                    self.stop()
                    raise ListenerError("HISTORICAL", update)
                if not self._running:
                    break
                else:
                    data = self.listener.snap()
                    if data:  # can return empty list
                        yield data
            else:
                # if f has finished, also stop the stream
                self.stop()
