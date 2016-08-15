import datetime
import logging

from ..resources.streamingresources import MarketBookCache, OrderBookCache
from ..utils import strp_betfair_integer_time


class Stream:
    """Separate stream class to hold market caches
    """

    __max_latency = 0.5

    def __init__(self, unique_id, stream_type, output_queue):
        self.unique_id = unique_id
        self.stream_type = stream_type
        self.output_queue = output_queue

        self._initial_clk = None
        self._clk = None
        self._caches = {}
        self._updates_processed = 0
        self._on_creation()

        self.time_created = datetime.datetime.utcnow()
        self.time_updated = datetime.datetime.utcnow()

    def on_heartbeat(self, data):
        self._update_clk(data)

    def on_resubscribe(self, data):
        self._update_clk(data)

    def on_subscribe(self, data, operation):
        self._update_clk(data)
        publish_time = strp_betfair_integer_time(data.get('pt'))

        if operation == 'mcm':
            market_books = data.get('mc', [])
            if market_books:
                self._process_market_books(market_books, publish_time)
            logging.info('[Stream: %s]: %s markets added' % (self.unique_id, len(market_books)))
        elif operation == 'ocm':
            order_books = data.get('oc')
            if order_books:
                self._process_order_books(order_books, publish_time)

    def on_update(self, data, operation):
        self._update_clk(data)

        publish_time = data.get('pt')
        latency = self._calc_latency(publish_time)
        if latency > self.__max_latency:
            logging.warning('[Stream: %s]: Latency high: %s' % (self.unique_id, latency))

        if operation == 'mcm':
            market_books = data.get('mc')
            self._process_market_books(market_books, publish_time)
        elif operation == 'ocm':
            order_books = data.get('oc')
            self._process_order_books(order_books, publish_time)

    def _process_market_books(self, market_books, publish_time):
        output_market_book = []
        for market_book in market_books:
            market_id = market_book.get('id')
            if market_book.get('img'):
                self._caches[market_id] = MarketBookCache(date_time_sent=publish_time, **market_book)
                logging.debug('[Stream: %s] %s added' % (self.unique_id, market_id))
            else:
                market_book_cache = self._caches.get(market_id)
                if market_book_cache:
                    market_book_cache.update_cache(market_book)
                    self._updates_processed += 1
                else:
                    logging.error('[Stream: %s] Received update for market not in stream: %s' %
                                  (self.unique_id, market_book))
            output_market_book.append(self._caches[market_id].create_market_book)

        self.output_queue.put(output_market_book)

    def _process_order_books(self, order_books, publish_time):
        output_order_book = []
        for order_book in order_books:
            market_id = order_book.get('id')
            order_book_cache = self._caches.get(market_id)
            if order_book_cache:
                order_book_cache.update_cache(order_book)
            else:
                self._caches[market_id] = OrderBookCache(**order_book)
                logging.info('[Stream: %s] %s added' % (self.unique_id, market_id))
            self._updates_processed += 1

            closed = order_book.get('closed')
            if closed:
                logging.info('[Stream: %s] %s closed' % (self.unique_id, market_id))
            output_order_book.append(self._caches[market_id].create_order_book)

        self.output_queue.put(output_order_book)

    def _on_creation(self):
        logging.info('[Stream: %s]: "%s" stream created' % (self.unique_id, self.stream_type))

    def _update_clk(self, data):
        (initial_clk, clk) = (data.get('initialClk'), data.get('clk'))
        if initial_clk:
            self._initial_clk = data.get('initialClk')
        if clk:
            self._clk = data.get('clk')
        self.time_updated = datetime.datetime.utcnow()

    @staticmethod
    def _calc_latency(publish_time):  # todo gmt /utc?
        return (datetime.datetime.utcnow() - strp_betfair_integer_time(publish_time)).total_seconds()
