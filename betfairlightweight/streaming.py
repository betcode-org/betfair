import socket
import ssl
import json
import logging
import datetime
import threading
import time

from .parse.apiparsestreaming import MarketBookCache, OrderBookCache


class StreamListener:
    """Stream listener, processes results from unlimited amount
     of sockets, holds streams which hold market_book caches
    """

    def __init__(self, output_queue=None):
        self.output_queue = output_queue

        self.streams = {}

        logging.info('[Listener]: Started')

    def on_data(self, raw_data, unique_id=None):
        """Called when raw data is received from connection.
        Override this method if you wish to manually handle
        the stream data

        :param raw_data: Received raw data
        :param unique_id: Unique id, used only on initial connection
        :return: Return False to stop stream and close connection
        """
        try:
            data = json.loads(raw_data)
        except ValueError:
            logging.error('value error: %s' % raw_data)
            return
        if not unique_id:
            unique_id = data.get('id')
        if self._error_handler(data, unique_id):
            return False

        operation = data.get('op')
        if operation == 'connection':
            self._on_connection(data, unique_id)
        elif operation == 'status':
            self._on_status(data, unique_id)
        elif operation == 'mcm' or operation == 'ocm':
            self._on_change_message(data, unique_id)
        else:
            logging.error('[Listener: %s]: Response error: %s' % (unique_id, data))

    def _on_connection(self, data, unique_id):
        """Called on collection operation

        :param data: Received data
        """
        self.connection_id = data.get('connectionId')
        logging.info('[Connect: %s]: connection_id: %s' % (unique_id, self.connection_id))

    def _on_status(self, data, unique_id):
        """Called on status operation

        :param data: Received data
        """
        status_code = data.get('statusCode')
        logging.info('[Subscription: %s]: %s' % (unique_id, status_code))

    def _on_change_message(self, data, unique_id):
        change_type = data.get('ct', 'UPDATE')
        operation = data.get('op')
        stream = self.streams.get(unique_id)
        if not stream:
            stream = self._add_stream(unique_id, operation)

        logging.debug('[Subscription: %s]: %s: %s' % (unique_id, change_type, data))

        if change_type == 'SUB_IMAGE':
            stream.on_subscribe(data)
        elif change_type == 'RESUB_DELTA':
            stream.on_resubscribe(data)
        elif change_type == 'HEARTBEAT':
            stream.on_heartbeat(data)
        elif change_type == 'UPDATE':
            stream.on_update(data)

    def _add_stream(self, unique_id, stream_type):
        self.streams[unique_id] = Stream(unique_id, stream_type, self.output_queue)
        return self.streams[unique_id]

    @staticmethod
    def _error_handler(data, unique_id):
        """Called when data first received

        :param data: Received data
        :return: True if error present
        """
        status_code = data.get('statusCode')
        connection_closed = data.get('connectionClosed')
        if status_code == 'FAILURE':
            logging.error('[Subscription: %s] %s: %s' %
                          (unique_id, data.get('errorCode'), data.get('errorMessage')))
            if connection_closed:
                time.sleep(1)
                return True


class Stream:
    """Separate stream class to hold market caches
    """

    __max_latency = 0.5

    def __init__(self, unique_id, stream_type, output_queue):
        self.unique_id = unique_id
        self.stream_type = stream_type
        self.output_queue = output_queue

        self.initial_clk = None
        self.clk = None
        self.caches = {}
        self.updates_processed = 0
        self._on_creation()

        self.time_created = datetime.datetime.now()
        self.time_updated = datetime.datetime.now()

    def on_subscribe(self, data):
        self._update_clk(data)
        publish_time = datetime.datetime.fromtimestamp(data.get('pt') / 1e3)

        if self.stream_type == 'mcm':
            market_books = data.get('mc', [])
            self._process_market_books(market_books, publish_time)
            logging.info('[Stream: %s]: %s markets added' % (self.unique_id, len(market_books)))
        elif self.stream_type == 'ocm':
            order_books = data.get('oc')
            self._process_order_books(order_books, publish_time)

    def on_update(self, data):
        self._update_clk(data)

        publish_time = data.get('pt')
        latency = self._calc_latency(publish_time)
        if latency > self.__max_latency:
            logging.warning('[Stream: %s]: Latency high: %s' % (self.unique_id, latency))

        if self.stream_type == 'mcm':
            market_books = data.get('mc')
            self._process_market_books(market_books, publish_time)
        elif self.stream_type == 'ocm':
            order_books = data.get('oc')
            self._process_order_books(order_books, publish_time)

    def _process_market_books(self, market_books, publish_time):
        for market_book in market_books:
            market_id = market_book.get('id')
            if market_book.get('img'):
                self.caches[market_id] = MarketBookCache(publish_time, market_book, market_book)
                logging.debug('[Stream: %s] %s added' % (self.unique_id, market_id))
            else:
                market_book_cache = self.caches.get(market_id)
                if market_book_cache:
                    market_book_cache.update_cache(market_book)
                    self.updates_processed += 1
                else:
                    logging.error('[Stream: %s] Received update for market not in stream: %s' %
                                  (self.unique_id, market_book))
            self.output_queue.put(self.caches[market_id].create_market_book)

    def _process_order_books(self, order_books, publish_time):
        for order_book in order_books:
            market_id = order_book.get('id')
            order_book_cache = self.caches.get(market_id)
            if order_book_cache:
                order_book_cache.update_cache(order_book)
                self.updates_processed += 1
            else:
                self.caches[market_id] = OrderBookCache(publish_time, order_book, order_book)

    def on_resubscribe(self, data):
        self._update_clk(data)

    def on_heartbeat(self, data):
        self._update_clk(data)

    def _on_creation(self):
        logging.info('[Stream: %s]: %s type stream created' % (self.unique_id, self.stream_type))

    def _update_clk(self, data):
        (initial_clk, clk) = (data.get('initialClk'), data.get('clk'))
        if initial_clk:
            self.initial_clk = data.get('initialClk')
        if clk:
            self.clk = data.get('clk')
        self.time_updated = datetime.datetime.now()

    @staticmethod
    def _calc_latency(publish_time):
        return (datetime.datetime.now() - datetime.datetime.fromtimestamp(publish_time / 1e3)).total_seconds()

    def __len__(self):
        return len(self.caches)


class BetfairStream:
    """Stream holder, socket connects to betfair,
    pushes any received data to listener
    """

    __host = 'stream-api.betfair.com'
    __port = 443
    __CRLF = '\r\n'
    __encoding = 'utf-8'

    def __init__(self, unique_id, listener, app_key, session_token, timeout, buffer_size):
        self.unique_id = unique_id
        self.listener = listener
        self.app_key = app_key
        self.session_token = session_token
        self.timeout = timeout
        self.buffer_size = buffer_size

        self.socket = None
        self.running = False

    def start(self, async=False):
        """Creates socket, waits for initial response, registers with
        listener and then starts read loop.

        :param async: If True new thread is started
        """
        self.running = True
        self.socket = self._create_socket()

        connection = self._receive_all()
        self.listener.on_data(connection, self.unique_id)

        if async:
            threading.Thread(name='BetfairStream', target=self._read_loop, daemon=True).start()
        else:
            self._read_loop()

    def stop(self):
        """Closes socket and stops read loop
        """
        self.running = False
        time.sleep(1)
        self.socket.close()
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

    def subscribe_to_markets(self, market_filter=None, market_data_filter=None, unique_id=None):
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
        """Creates ssl socket and connects to stream api.

        :return: Connected socket.
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
        while self.running:
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
        logging.warning('_read_loop ended: %s' % self.unique_id)

    def _receive_all(self):
        """Whilst socket is running receives data from socket,
        till CRLF is detected.

        :return: Decoded data.
        """
        (data, part) = ('', '')
        while self.running and part[-2:] != bytes(self.__CRLF, encoding=self.__encoding):
            part = self.socket.recv(self.buffer_size)
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
        self.socket.send(message_dumped.encode())
