import datetime
import logging
import time

from ..resources.streamingresources import (
    MarketBookCache,
    OrderBookCache,
)

logger = logging.getLogger(__name__)


class BaseStream(object):
    """Separate stream class to hold market/order caches
    """

    _lookup = 'mc'

    def __init__(self, unique_id, output_queue, max_latency, lightweight):
        self.unique_id = unique_id
        self.output_queue = output_queue
        self._max_latency = max_latency
        self._lightweight = lightweight

        self._initial_clk = None
        self._clk = None
        self._caches = {}
        self._updates_processed = 0
        self._on_creation()

        self.time_created = datetime.datetime.utcnow()
        self.time_updated = datetime.datetime.utcnow()

    def on_subscribe(self, data):
        self._update_clk(data)
        publish_time = data.get('pt')

        book_data = data.get(self._lookup)
        if book_data:
            self._process(book_data, publish_time)
        logger.info('[Stream: %s]: %s %s added' % (self.unique_id, len(self._caches), self._lookup))

    def on_heartbeat(self, data):
        self._update_clk(data)

    def on_resubscribe(self, data):
        self._update_clk(data)

    def on_update(self, data):
        self._update_clk(data)

        publish_time = data.get('pt')
        latency = self._calc_latency(publish_time)
        if latency > self._max_latency:
            logger.warning('[Stream: %s]: Latency high: %s' % (self.unique_id, latency))

        book_data = data.get(self._lookup)
        self._process(book_data, publish_time)

    def clear_cache(self):
        self._caches.clear()

    def _on_creation(self):
        logger.info('[Stream: %s]: "%s" created' % (self.unique_id, self))

    def _process(self, book_data, publish_time):
        pass

    def _update_clk(self, data):
        (initial_clk, clk) = (data.get('initialClk'), data.get('clk'))
        if initial_clk:
            self._initial_clk = initial_clk
        if clk:
            self._clk = clk
        self.time_updated = datetime.datetime.utcnow()

    @staticmethod
    def _calc_latency(publish_time):
        return time.time() - publish_time / 1e3

    def __str__(self):
        return '<BaseStream>'

    def __repr__(self):
        return str(self)


class MarketStream(BaseStream):

    _lookup = 'mc'

    def _process(self, market_books, publish_time):
        output_market_book = []
        for market_book in market_books:
            market_id = market_book.get('id')
            if market_book.get('img'):
                self._caches[market_id] = MarketBookCache(publish_time=publish_time, **market_book)
                logger.info('[MarketStream: %s] %s added' % (self.unique_id, market_id))
            else:
                market_book_cache = self._caches.get(market_id)
                if market_book_cache:
                    market_book_cache.update_cache(market_book, publish_time)
                    self._updates_processed += 1
                else:
                    logger.error('[MarketStream: %s] Received update for market not in cache: %s' %
                                 (self.unique_id, market_book))
            output_market_book.append(
                self._caches[market_id].create_market_book(self.unique_id, market_book, self._lightweight)
            )

        self.output_queue.put(output_market_book)

    def __str__(self):
        return 'MarketStream'

    def __repr__(self):
        return '<MarketStream [%s]>' % len(self._caches)


class OrderStream(BaseStream):

    _lookup = 'oc'

    def _process(self, order_books, publish_time):
        output_order_book = []
        for order_book in order_books:
            market_id = order_book.get('id')
            order_book_cache = self._caches.get(market_id)
            if order_book_cache:
                order_book_cache.update_cache(order_book, publish_time)
            else:
                self._caches[market_id] = OrderBookCache(publish_time=publish_time, **order_book)
                logger.info('[OrderStream: %s] %s added' % (self.unique_id, market_id))
            self._updates_processed += 1

            output_order_book.append(
                self._caches[market_id].create_order_book(self.unique_id, order_book, self._lightweight)
            )

        self.output_queue.put(output_order_book)

    def __str__(self):
        return 'OrderStream'

    def __repr__(self):
        return '<OrderStream [%s]>' % len(self._caches)
