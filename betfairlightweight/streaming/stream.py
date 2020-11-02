import datetime
import logging
import time
import queue

from .cache import MarketBookCache, OrderBookCache

logger = logging.getLogger(__name__)

MAX_CACHE_AGE = 60 * 60 * 8


class BaseStream:
    """Separate stream class to hold market/order caches"""

    _lookup = "mc"
    _name = "Stream"

    def __init__(self, listener: object):
        self._listener = listener

        self._initial_clk = None
        self._clk = None
        self._caches = {}
        self._updates_processed = 0
        self._on_creation()

        self.time_created = datetime.datetime.utcnow()
        self.time_updated = datetime.datetime.utcnow()

    def on_subscribe(self, data: dict) -> None:
        self._update_clk(data)
        publish_time = data.get("pt")

        if self._lookup in data:
            self._process(data[self._lookup], publish_time)
        logger.info(
            "[%s: %s]: %s %s added"
            % (self, self.unique_id, len(self._caches), self._lookup)
        )

    def on_heartbeat(self, data: dict) -> None:
        self._update_clk(data)

    def on_resubscribe(self, data: dict) -> None:
        self.on_update(data)
        logger.info(
            "[%s: %s]: %s %s resubscribed"
            % (self, self.unique_id, len(self._caches), self._lookup)
        )

    def on_update(self, data: dict) -> None:
        self._update_clk(data)

        publish_time = data["pt"]
        latency = self._calc_latency(publish_time)
        if self._max_latency and latency > self._max_latency:
            logger.warning(
                "[%s: %s]: Latency high: %s" % (self, self.unique_id, latency)
            )

        if self._lookup in data:
            img = self._process(data[self._lookup], publish_time)

            # remove stale cache data on any new img to prevent memory leaks (only live)
            if img and self.unique_id != 0:
                self.clear_stale_cache(publish_time)

    def clear_cache(self) -> None:
        self._caches.clear()

    def clear_stale_cache(self, publish_time: int) -> None:
        _to_remove = []
        for cache in self._caches.values():
            if (
                cache.closed
                and (publish_time - cache.publish_time) / 1e3 > MAX_CACHE_AGE
            ):
                _to_remove.append(cache.market_id)
        for market_id in _to_remove:
            del self._caches[market_id]
            logger.info(
                "[%s: %s]: %s removed, %s markets in cache"
                % (self, self.unique_id, market_id, len(self._caches))
            )

    def snap(self, market_ids: list = None) -> list:
        return [
            cache.create_resource(self.unique_id, self._lightweight, snap=True)
            for cache in list(self._caches.values())
            if market_ids is None or cache.market_id in market_ids
        ]

    def on_process(self, output: list) -> None:
        if self.output_queue:
            self.output_queue.put(output)

    def _on_creation(self) -> None:
        logger.info('[%s: %s]: "%s" created' % (self, self.unique_id, self))

    def _process(self, data: dict, publish_time: int) -> bool:
        # Return True if new img within data
        pass

    def _update_clk(self, data: dict) -> None:
        (initial_clk, clk) = (data.get("initialClk"), data.get("clk"))
        if initial_clk:
            self._initial_clk = initial_clk
        if clk:
            self._clk = clk
        self.time_updated = datetime.datetime.utcnow()

    @property
    def unique_id(self) -> int:
        return self._listener.stream_unique_id

    @property
    def output_queue(self) -> queue.Queue:
        return self._listener.output_queue

    @property
    def _max_latency(self) -> float:
        return self._listener.max_latency

    @property
    def _lightweight(self) -> bool:
        return self._listener.lightweight

    @staticmethod
    def _calc_latency(publish_time: int) -> float:
        return time.time() - publish_time / 1e3

    def __len__(self) -> int:
        return len(self._caches)

    def __str__(self) -> str:
        return "{0}".format(self._name)

    def __repr__(self) -> str:
        return "<{0} [{1}]>".format(self._name, len(self))


class MarketStream(BaseStream):

    _lookup = "mc"
    _name = "MarketStream"

    def _process(self, data: list, publish_time: int) -> bool:
        output_market_book, img = [], False
        for market_book in data:
            market_id = market_book["id"]
            full_image = market_book.get("img", False)
            market_book_cache = self._caches.get(market_id)

            if (
                full_image or market_book_cache is None
            ):  # historic data does not contain img
                img = True
                if "marketDefinition" not in market_book:
                    logger.error(
                        "[%s: %s]: Unable to add %s to cache due to marketDefinition "
                        "not being present (make sure EX_MARKET_DEF is requested)"
                        % (self, self.unique_id, market_id)
                    )
                    continue
                market_book_cache = MarketBookCache(
                    publish_time=publish_time, **market_book
                )
                self._caches[market_id] = market_book_cache
                logger.info(
                    "[%s: %s]: %s added, %s markets in cache"
                    % (self, self.unique_id, market_id, len(self._caches))
                )

            market_book_cache.update_cache(market_book, publish_time)
            self._updates_processed += 1

            output_market_book.append(
                market_book_cache.create_resource(self.unique_id, self._lightweight)
            )
        self.on_process(output_market_book)
        return img


class OrderStream(BaseStream):

    _lookup = "oc"
    _name = "OrderStream"

    def _process(self, data: list, publish_time: int) -> bool:
        output_order_book, img = [], False
        for order_book in data:
            market_id = order_book["id"]
            full_image = order_book.get("fullImage", False)
            order_book_cache = self._caches.get(market_id)

            if full_image or order_book_cache is None:
                img = True
                order_book_cache = OrderBookCache(
                    publish_time=publish_time, **order_book
                )
                self._caches[market_id] = order_book_cache
                logger.info(
                    "[%s: %s]: %s added, %s markets in cache"
                    % (self, self.unique_id, market_id, len(self._caches))
                )

            order_book_cache.update_cache(order_book, publish_time)
            self._updates_processed += 1

            output_order_book.append(
                order_book_cache.create_resource(self.unique_id, self._lightweight)
            )
        self.on_process(output_order_book)
        return img
