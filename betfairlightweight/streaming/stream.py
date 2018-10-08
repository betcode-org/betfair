import datetime
import logging
import time

from .cache import (
    MarketBookCache,
    OrderBookCache,
    RaceCache,
)

logger = logging.getLogger(__name__)


class BaseStream(object):
    """Separate stream class to hold market/order caches
    """

    _lookup = 'mc'

    def __init__(self, listener):
        self._listener = listener

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

        if self._lookup in data:
            self._process(data[self._lookup], publish_time)
        logger.info('[Stream: %s]: %s %s added' % (self.unique_id, len(self._caches), self._lookup))

    def on_heartbeat(self, data):
        self._update_clk(data)

    def on_resubscribe(self, data):
        self.on_update(data)
        logger.info('[Stream: %s]: %s %s resubscribed' % (self.unique_id, len(self._caches), self._lookup))

    def on_update(self, data):
        self._update_clk(data)

        publish_time = data['pt']
        latency = self._calc_latency(publish_time)
        if latency > self._max_latency:
            logger.warning('[Stream: %s]: Latency high: %s' % (self.unique_id, latency))

        if self._lookup in data:
            self._process(data[self._lookup], publish_time)

    def clear_cache(self):
        self._caches.clear()

    def snap(self, market_ids=None):
        return [
            cache.create_resource(self.unique_id, None, self._lightweight) for cache in list(self._caches.values())
            if market_ids is None or cache.market_id in market_ids
        ]

    def on_process(self, output):
        if self.output_queue:
            self.output_queue.put(output)

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

    @property
    def unique_id(self):
        return self._listener.stream_unique_id

    @property
    def output_queue(self):
        return self._listener.output_queue

    @property
    def _max_latency(self):
        return self._listener.max_latency

    @property
    def _lightweight(self):
        return self._listener.lightweight

    @staticmethod
    def _calc_latency(publish_time):
        return time.time() - publish_time / 1e3

    def __len__(self):
        return len(self._caches)

    def __str__(self):
        return 'BaseStream'

    def __repr__(self):
        return '<BaseStream>'


class MarketStream(BaseStream):

    _lookup = 'mc'

    def _process(self, market_books, publish_time):
        output_market_book = []
        for market_book in market_books:
            market_id = market_book['id']
            market_book_cache = self._caches.get(market_id)

            if market_book.get('img') or market_book_cache is None:  # historic data does not contain img
                market_book_cache = MarketBookCache(publish_time=publish_time, **market_book)
                self._caches[market_id] = market_book_cache
                logger.info('[MarketStream: %s] %s added, %s markets in cache' %
                            (self.unique_id, market_id, len(self._caches)))

            market_book_cache.update_cache(market_book, publish_time)
            self._updates_processed += 1

            output_market_book.append(
                market_book_cache.create_resource(self.unique_id, market_book, self._lightweight)
            )
        self.on_process(output_market_book)

    def __str__(self):
        return 'MarketStream'

    def __repr__(self):
        return '<MarketStream [%s]>' % len(self)


class OrderStream(BaseStream):

    _lookup = 'oc'

    def _process(self, order_books, publish_time):
        output_order_book = []
        for order_book in order_books:
            market_id = order_book['id']
            order_book_cache = self._caches.get(market_id)

            if order_book_cache is None:
                order_book_cache = OrderBookCache(publish_time=publish_time, **order_book)
                self._caches[market_id] = order_book_cache
                logger.info('[OrderStream: %s] %s added, %s markets in cache' %
                            (self.unique_id, market_id, len(self._caches)))

            order_book_cache.update_cache(order_book, publish_time)
            self._updates_processed += 1

            output_order_book.append(
                self._caches[market_id].create_resource(self.unique_id, order_book, self._lightweight)
            )
        self.on_process(output_order_book)

    def __str__(self):
        return 'OrderStream'

    def __repr__(self):
        return '<OrderStream [%s]>' % len(self)


class RaceStream(BaseStream):

    """
    Cache contains latest update:
        marketId: RaceCache
    """

    _lookup = 'rc'

    def on_subscribe(self, data):
        """The initial message returned after
        a subscribe - This will currently not
        contain any Race Changes (rc) but may
        do in the future"""
        pass

    def _process(self, race_updates, publish_time):
        output = []
        for update in race_updates:
            market_id = update['mid']

            race_cache = self._caches.get(market_id)
            if race_cache is None:
                race_cache = RaceCache(publish_time=publish_time, **update)
                self._caches[market_id] = race_cache
                logger.info('[RaceStream: %s] %s added' % (self.unique_id, market_id))
            race_cache.update_cache(update, publish_time)
            self._updates_processed += 1

            output.append(
                race_cache.create_resource(self.unique_id, update, self._lightweight)
            )
        self.on_process(output)

    def __str__(self):
        return 'RaceStream'

    def __repr__(self):
        return '<RaceStream [%s]>' % len(self)
