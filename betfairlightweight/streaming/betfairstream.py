import ujson as json
import threading
import socket
import ssl
import datetime

from ..exceptions import SocketError
from ..compat import is_py3


class BetfairStream(object):
    """Socket holder, connects to betfair and
    pushes any received data to listener
    """

    __host = 'stream-api.betfair.com'
    __port = 443
    __CRLF = '\r\n'
    __encoding = 'utf-8'

    def __init__(self, unique_id, listener, app_key, session_token, timeout, buffer_size, description):
        self._unique_id = unique_id
        self.listener = listener
        self.app_key = app_key
        self.session_token = session_token
        self.timeout = timeout
        self.buffer_size = buffer_size
        self.description = description
        self.receive_count = 0
        self.datetime_last_received = None

        self._socket = None
        self._running = False

    def start(self, async=False):
        """Starts read loop, new thread if async and
        connects/authenticates if not already running.

        :param async: If True new thread is started
        """
        if not self._running:
            self._connect()
            self.authenticate()
        if async:
            t = threading.Thread(name=self.description, target=self._read_loop)
            t.daemon = False
            t.start()
        else:
            self._read_loop()

    def stop(self):
        """Stops read loop and closes socket if it has been created.
        """
        self._running = False

        if self._socket is not None:
            try:
                self._socket.shutdown(2)  # SHUT_RDWR
            except OSError:
                pass

    def authenticate(self):
        """Authentication request.
        """
        unique_id = self.new_unique_id()
        message = {
            'op': 'authentication',
            'id': unique_id,
            'appKey': self.app_key,
            'session': self.session_token,
        }
        self._send(message)
        return unique_id

    def heartbeat(self):
        """Heartbeat request to keep session alive.
        """
        unique_id = self.new_unique_id()
        message = {
            'op': 'heartbeat',
            'id': unique_id,
        }
        self._send(message)
        return unique_id

    def subscribe_to_markets(self, market_filter, market_data_filter, initial_clk=None, clk=None,
                             conflate_ms=None, heartbeat_ms=None, segmentation_enabled=True):
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
            'op': 'marketSubscription',
            'id': unique_id,
            'marketFilter': market_filter,
            'marketDataFilter': market_data_filter,
            'initialClk': initial_clk,
            'clk': clk,
            'conflateMs': conflate_ms,
            'heartbeatMs': heartbeat_ms,
            'segmentationEnabled': segmentation_enabled,
        }
        self.listener.register_stream(unique_id, 'marketSubscription')
        self._send(message)
        return unique_id

    def subscribe_to_orders(self, order_filter=None, initial_clk=None, clk=None, conflate_ms=None,
                            heartbeat_ms=None, segmentation_enabled=True):
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
            'op': 'orderSubscription',
            'id': unique_id,
            'orderFilter': order_filter,
            'initialClk': initial_clk,
            'clk': clk,
            'conflateMs': conflate_ms,
            'heartbeatMs': heartbeat_ms,
            'segmentationEnabled': segmentation_enabled,
        }
        self.listener.register_stream(unique_id, 'orderSubscription')
        self._send(message)
        return unique_id

    def new_unique_id(self):
        self._unique_id += 1
        return self._unique_id

    def _connect(self):
        """Creates socket and sets running to True.
        """
        self._socket = self._create_socket()
        self._running = True

    def _create_socket(self):
        """Creates ssl socket, connects to stream api and
        sets timeout.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = ssl.wrap_socket(s)
        s.connect((self.__host, self.__port))
        s.settimeout(self.timeout)
        return s

    def _read_loop(self):
        """Read loop, splits by CRLF and pushes received data
        to _data.
        """
        while self._running:
            try:
                received_data_raw = self._receive_all()
                if self._running:
                    self.receive_count += 1
                    self.datetime_last_received = datetime.datetime.utcnow()
                    received_data_split = received_data_raw.split(self.__CRLF)
                    for received_data in received_data_split:
                        if received_data:
                            self._data(received_data)
            except (socket.timeout, socket.error) as e:
                self.stop()
                raise SocketError('[Connect: %s]: Socket %s' % (self._unique_id, e))

    def _receive_all(self):
        """Whilst socket is running receives data from socket,
        till CRLF is detected.
        """
        (data, part) = ('', '')
        if is_py3:
            crlf_bytes = bytes(self.__CRLF, encoding=self.__encoding)
        else:
            crlf_bytes = self.__CRLF

        while self._running and part[-2:] != crlf_bytes:
            part = self._socket.recv(self.buffer_size)
            if part:
                data += part.decode(self.__encoding)
        return data

    def _data(self, received_data):
        """Sends data to listener, if False is returned; socket
        is closed.

        :param received_data: Decoded data received from socket.
        """
        if self.listener.on_data(received_data) is False:
            self.stop()

    def _send(self, message):
        """If not running connects socket and
        authenticates. Adds CRLF and sends message
        to Betfair.

        :param message: Data to be sent to Betfair.
        """
        if not self._running:
            self._connect()
            self.authenticate()
        message_dumped = json.dumps(message) + self.__CRLF
        self._socket.send(message_dumped.encode())

    def __str__(self):
        return '<BetfairStream [%s]>' % ('running' if self._running else 'not running')

    def __repr__(self):
        return '<BetfairStream>'
