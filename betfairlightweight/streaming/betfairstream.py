import json
import threading
import time
import logging
import socket
import ssl


class BetfairStream:
    """Stream holder, socket connects to betfair,
    pushes any received data to listener
    """

    __host = 'stream-api.betfair.com'
    __port = 443
    __CRLF = '\r\n'
    __encoding = 'utf-8'

    def __init__(self, unique_id, listener, app_key, session_token, timeout, buffer_size, description):
        self.unique_id = unique_id
        self.listener = listener
        self.app_key = app_key
        self.session_token = session_token
        self.timeout = timeout
        self.buffer_size = buffer_size
        self.description = description

        self._socket = None
        self._running = False

    def start(self, async=False):
        """Creates socket, registers with listener, waits for
        initial response and then starts read loop.

        :param async: If True new thread is started
        """
        self._running = True
        self.listener.register_stream(self.unique_id, self.description)
        self._socket = self._create_socket()

        connection_string = self._receive_all()
        self.listener.on_data(connection_string, self.unique_id)

        if async:
            threading.Thread(name='BetfairStream', target=self._read_loop, daemon=True).start()
        else:
            self._read_loop()

    def stop(self):
        """Closes socket and stops read loop
        """
        self._running = False
        time.sleep(1)
        self._socket.close()
        logging.info('[Connect: %s]: Socket closed' % self.unique_id)

    def authenticate(self, unique_id=None):
        """Authentication request.

        :param unique_id: If not supplied 1 is used.
        """
        message = {'op': 'authentication',
                   'id': self.unique_id if not unique_id else unique_id,
                   'appKey': self.app_key,
                   'session': self.session_token}
        self._send(message)

    def heartbeat(self, unique_id=None):
        """Heartbeat request to keep session alive.

        :param unique_id: self.unique_id used if not supplied.
        """
        message = {'op': 'heartbeat',
                   'id': self.unique_id if not unique_id else unique_id}
        self._send(message)

    def subscribe_to_markets(self, market_filter, market_data_filter, unique_id=None):
        """Market subscription request.

        :param market_filter: Market filter.
        :param market_data_filter: Market data filter.
        :param unique_id: self.unique_id used if not supplied.
        """
        message = {'op': 'marketSubscription',
                   'id': self.unique_id if not unique_id else unique_id,
                   'marketFilter': market_filter,
                   'marketDataFilter': market_data_filter}
        self._send(message)

    def subscribe_to_orders(self, unique_id=None):
        """Order subscription request.

        :param unique_id: self.unique_id used if not supplied.
        """
        message = {'op': 'orderSubscription',
                   'id': self.unique_id if not unique_id else unique_id}
        self._send(message)

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
                received_data_split = received_data_raw.split(self.__CRLF)
                for received_data in received_data_split:
                    if received_data:
                        self._data(received_data)
            except socket.timeout:
                logging.warning('[Connect: %s]: Socket timeout' % self.unique_id)
            except socket.error as e:
                logging.ERROR('[Connect: %s]: Socket error, %s' % (self.unique_id, e))
                break
        logging.warning('[Connect: %s]: _read_loop ended' % self.unique_id)

    def _receive_all(self):
        """Whilst socket is running receives data from socket,
        till CRLF is detected.
        """
        (data, part) = ('', '')
        while self._running and part[-2:] != bytes(self.__CRLF, encoding=self.__encoding):
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
        """Adds CRLF and sends message to Betfair.

        :param message: Data to be sent to Betfair.
        """
        message_dumped = json.dumps(message) + self.__CRLF
        self._socket.send(message_dumped.encode())
