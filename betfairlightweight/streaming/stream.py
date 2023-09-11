import datetime
import logging
import time
from typing import Optional

from .cache import CricketMatchCache, MarketBookCache, OrderBookCache, RaceCache

logger = logging.getLogger(__name__)

MAX_CACHE_AGE = 60 * 60 * 8  # 8hrs


class BaseStream:
    """Separate stream class to hold market/order caches"""

    _lookup = "mc"
    _name = "Stream"

    def __init__(self, listener: object, unique_id: int):
        self._listener = listener
        self.unique_id = unique_id
        self.output_queue = listener.output_queue
        self.update_clk = listener.update_clk
        self._max_latency = listener.max_latency
        self._lightweight = listener.lightweight
        self._calculate_market_tv = listener.calculate_market_tv
        self._cumulative_runner_tv = listener.cumulative_runner_tv
        self._order_updates_only = listener.order_updates_only

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
            "[%s: %s]: %s %s added",
            self,
            self.unique_id,
            len(self._caches),
            self._lookup,
        )

    def on_heartbeat(self, data: dict) -> None:
        self._update_clk(data)

    def on_resubscribe(self, data: dict) -> None:
        self.on_update(data)
        logger.info(
            "[%s: %s]: %s %s resubscribed",
            self,
            self.unique_id,
            len(self._caches),
            self._lookup,
        )

    def on_update(self, data: dict) -> None:
        if self.update_clk:
            self._update_clk(data)

        publish_time = data["pt"]
        if self._max_latency:
            latency = self._calc_latency(publish_time)
            if latency > self._max_latency:
                logger.warning(
                    "[%s: %s]: Latency high: %s", self, self.unique_id, latency
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
                "[%s: %s]: %s removed, %s markets in cache",
                self,
                self.unique_id,
                market_id,
                len(self._caches),
            )

    def snap(self, market_ids: list = None, publish_time: Optional[int] = None) -> list:
        # yes you can avoid the if and have fewer lines of code but it's faster
        # to treat these cases separately as you can avoid list(...) and some
        # conditionals!
        if market_ids:
            return [
                cache.create_resource(
                    self.unique_id, snap=True, publish_time=publish_time
                )
                for market_id in market_ids
                if (cache := self._caches.get(market_id)) is not None and cache.active
            ]
        else:
            return [
                cache.create_resource(
                    self.unique_id, snap=True, publish_time=publish_time
                )
                for cache in list(self._caches.values())
                if cache.active
            ]

    def on_process(self, caches: list, publish_time: Optional[int] = None) -> None:
        if self.output_queue:
            output = [
                cache.create_resource(
                    self.unique_id, snap=False, publish_time=publish_time
                )
                for cache in caches
            ]
            self.output_queue.put(output)

    def _on_creation(self) -> None:
        logger.info('[%s: %s]: "%s" created', self, self.unique_id, self)

    def _process(self, data: list, publish_time: int) -> bool:
        # Return True if new img within data
        pass

    def _update_clk(self, data: dict) -> None:
        (initial_clk, clk) = (data.get("initialClk"), data.get("clk"))
        if initial_clk:
            self._initial_clk = initial_clk
        if clk:
            self._clk = clk
        self.time_updated = datetime.datetime.utcnow()

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
        caches, img = [], False
        for market_book in data:
            market_id = market_book["id"]
            full_image = market_book.get("img", False)
            market_book_cache = self._caches.get(market_id)

            if (
                full_image or market_book_cache is None
            ):  # historic data does not contain img
                img = True
                if "marketDefinition" not in market_book:
                    logger.warning(
                        "[%s: %s]: Missing marketDefinition on market %s resulting "
                        "in potential missing data in the MarketBook (make sure "
                        "EX_MARKET_DEF is requested)",
                        self,
                        self.unique_id,
                        market_id,
                    )
                market_book_cache = MarketBookCache(
                    market_id,
                    publish_time,
                    self._lightweight,
                    self._calculate_market_tv,
                    self._cumulative_runner_tv,
                )
                self._caches[market_id] = market_book_cache
                logger.info(
                    "[%s: %s]: %s added, %s markets in cache",
                    self,
                    self.unique_id,
                    market_id,
                    len(self._caches),
                )

            market_book_cache.update_cache(market_book, publish_time, True)
            caches.append(market_book_cache)
            self._updates_processed += 1
        self.on_process(caches)
        return img


class OrderStream(BaseStream):
    _lookup = "oc"
    _name = "OrderStream"

    def _process(self, data: list, publish_time: int) -> bool:
        caches, img = [], False
        for order_book in data:
            market_id = order_book["id"]
            full_image = order_book.get("fullImage", False)
            order_book_cache = self._caches.get(market_id)

            if full_image or order_book_cache is None:
                img = True
                order_book_cache = OrderBookCache(
                    market_id, publish_time, self._lightweight
                )
                self._caches[market_id] = order_book_cache
                logger.info(
                    "[%s: %s]: %s added, %s markets in cache",
                    self,
                    self.unique_id,
                    market_id,
                    len(self._caches),
                )

            order_book_cache.update_cache(order_book, publish_time)
            caches.append(order_book_cache)
            self._updates_processed += 1
        if self._order_updates_only:
            self.on_process(caches, publish_time)
        else:
            self.on_process(caches)
        return img


class RaceStream(BaseStream):

    """
    Cache contains latest update:
        marketId: RaceCache
    """

    _lookup = "rc"
    _name = "RaceStream"

    def on_subscribe(self, data: dict) -> None:
        """The initial message returned after
        a subscribe - This will currently not
        contain any Race Changes (rc) but may
        do in the future"""
        pass

    def _process(self, race_updates: list, publish_time: int) -> bool:
        caches, img = [], False  # todo cache.closed / img=True
        for update in race_updates:
            market_id = update["mid"]
            race_cache = self._caches.get(market_id)

            if race_cache is None:
                race_id = update.get("id")
                race_cache = RaceCache(
                    market_id, publish_time, race_id, self._lightweight
                )
                self._caches[market_id] = race_cache
                logger.info(
                    "[%s: %s]: %s added, %s markets in cache",
                    self,
                    self.unique_id,
                    market_id,
                    len(self._caches),
                )

            race_cache.update_cache(update, publish_time)
            caches.append(race_cache)
            self._updates_processed += 1
        self.on_process(caches)
        return img


class CricketStream(BaseStream):
    _lookup = "cc"
    _name = "CricketStream"

    def _process(self, cricket_changes: list, publish_time: int) -> bool:
        caches, img = [], False
        for cricket_change in cricket_changes:
            market_id = cricket_change["marketId"]
            event_id = cricket_change["eventId"]
            cricket_match_cache = self._caches.get(market_id)

            if cricket_match_cache is None:
                cricket_match_cache = CricketMatchCache(
                    market_id, event_id, publish_time, self._lightweight
                )
                self._caches[market_id] = cricket_match_cache
                logger.info(
                    "[%s: %s]: %s added, %s markets in cache",
                    self,
                    self.unique_id,
                    market_id,
                    len(self._caches),
                )

            cricket_match_cache.update_cache(cricket_change, publish_time)
            caches.append(cricket_match_cache)
            self._updates_processed += 1
        self.on_process(caches)
        return img
