import socket
import ssl
import json
import logging
import datetime
import threading
import time

from .parse.apiparsestreaming import MarketBookCache


class StreamListener:
    """Stream listener, processes results from a single socket,
    holds stream which holds market_book caches
    """

    def __init__(self, unique_id, output_queue=None):
        self.unique_id = unique_id
        self.output_queue = output_queue

        self.authenticated = False
        self.connection_id = None
        self.stream = None

        logging.info('[Listener: %s]: Started' % unique_id)

    def on_data(self, raw_data):
        """Called when raw data is received from connection.
        Override this method if you wish to manually handle
        the stream data

        :param raw_data: Received raw data
        :return: Return False to stop stream and close connection
        """
        try:
            data = json.loads(raw_data)
        except ValueError:
            logging.error('value error: %s' % raw_data)
            return
        if self._error_handler(data):
            return False

        operation = data.get('op')
        if operation == 'connection':
            self._on_connection(data)
        elif operation == 'status':
            self._on_status(data)
        elif operation == 'mcm' or operation == 'ocm':
            self._on_change_message(data)
        else:
            logging.error('[Listener: %s]: Response error: %s' % (self.unique_id, data))

    def _on_connection(self, data):
        """Called on collection operation

        :param data: Received data
        """
        self.connection_id = data.get('connectionId')
        logging.info('[Connect: %s]: connection_id: %s' % (self.unique_id, self.connection_id))

    def _on_status(self, data):
        """Called on status operation

        :param data: Received data
        """
        status_code = data.get('statusCode')

        if data.get('id') == 1 and status_code == 'SUCCESS':
            logging.info('[Authenticating: %s]: %s' % (self.unique_id, status_code))
            self.authenticated = True

        elif status_code == 'SUCCESS':
            logging.info('[Subscription: %s]: %s' % (self.unique_id, status_code))

    def _on_change_message(self, data):
        change_type = data.get('ct', 'UPDATE')
        operation = data.get('op')
        stream = self.stream
        if not stream:
            stream = self._add_stream(operation)

        logging.debug('[Subscription: %s]: %s: %s' % (self.unique_id, change_type, data))

        if change_type == 'SUB_IMAGE':
            stream.on_subscribe(data)
        elif change_type == 'RESUB_DELTA':
            stream.on_resubscribe(data)
        elif change_type == 'HEARTBEAT':
            stream.on_heartbeat(data)
        elif change_type == 'UPDATE':
            stream.on_update(data)

    def _add_stream(self, stream_type):
        self.stream = Stream(self.unique_id, stream_type, self.output_queue)
        return self.stream

    def _error_handler(self, data):
        """Called when data first received

        :param data: Received data
        :return: True if error present
        """
        status_code = data.get('statusCode')
        connection_closed = data.get('connectionClosed')
        if status_code == 'FAILURE':
            logging.error('[Subscription: %s] %s: %s' %
                          (self.unique_id, data.get('errorCode'), data.get('errorMessage')))
            if connection_closed:
                time.sleep(1)
                return True


class Stream:
    """Separate stream class to hold market caches
    """

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

        latency = ((datetime.datetime.now() - datetime.datetime.fromtimestamp(publish_time / 1e3)).total_seconds())
        if latency > 1.5:
            logging.warning('Latency high: %s' % latency)

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
                logging.debug('[Stream: %s] %s added to stream' % (self.unique_id, market_id))
            else:
                market_book_cache = self.caches.get(market_id)
                if market_book_cache:
                    market_book_cache.update_cache(market_book)
                    self.updates_processed += 1
                else:
                    logging.error('[Stream: %s] Received update for market not in stream: %s' %
                                  (self.unique_id, market_book))
            self.output_queue.put(self.caches[market_id].serialise)

    def _process_order_books(self, order_books, publish_time):
        pass

    def on_resubscribe(self, data):
        self._update_clk(data)

    def on_heartbeat(self, data):
        self._update_clk(data)

    def _on_creation(self):
        logging.info('[Stream: %s]: Created' % self.unique_id)

    def _update_clk(self, data):
        (initial_clk, clk) = (data.get('initialClk'), data.get('clk'))
        if initial_clk:
            self.initial_clk = data.get('initialClk')
        if clk:
            self.clk = data.get('clk')
        self.time_updated = datetime.datetime.now()

    def __len__(self):
        return len(self.caches)


class BetfairStream:
    """Stream holder, socket connects to betfair,
    pushes any received data to listener
    """

    __host = 'stream-api.betfair.com'
    __port = 443

    def __init__(self, unique_id, listener=None):
        self.listener = listener if listener else StreamListener(unique_id)
        self.unique_id = unique_id
        self.socket = None
        self.running = False

    def start(self, async=False):
        self.running = True
        self.socket = self._create_socket()
        if async:
            threading.Thread(name='BetfairStream', target=self._read_loop, daemon=True).start()
        else:
            self._read_loop()

    def stop(self):
        self.running = False
        self.socket.close()
        logging.info('[Connect: %s]: Socket closed' % self.unique_id)

    def authenticate(self, app_key, session_token):
        message = {'op': 'authentication',
                   'id': 1,
                   'appKey': app_key,
                   'session': session_token}
        self._send(message)

    def heartbeat(self):
        message = {'op': 'heartbeat',
                   'id': self.unique_id}
        self._send(message)

    def subscribe_to_market(self, market_filter=None, market_data_filter=None):
        message = {'op': 'marketSubscription',
                   'id': self.unique_id,
                   'marketFilter': market_filter,
                   'marketDataFilter': market_data_filter}
        self._send(message)

    def subscribe_to_orders(self):
        message = {'op': 'orderSubscription',
                   'id': self.unique_id}
        self._send(message)

    def _create_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = ssl.wrap_socket(s)
        s.connect((self.__host, self.__port))
        return s

    def _read_loop(self):
        while self.running:
            try:
                received_data_raw = self._receive_all()
                received_data_split = received_data_raw.split('\r\n')
                for received_data in received_data_split:
                    if received_data:
                        self._data(received_data)
            except OSError:
                break
        logging.warning('_read_loop ended: %s' % self.unique_id)

    def _receive_all(self):
        (data, part) = ('', '')
        while self.running and part[-2:] != b'\r\n':
            part = self.socket.recv(1024)
            if part:
                data += part.decode('utf-8')
        return data

    def _data(self, received_data):
        if self.listener.on_data(received_data) is False:
            self.stop()

    def _send(self, message):
        message_dumped = json.dumps(message)+'\r\n'
        self.socket.send(message_dumped.encode())
