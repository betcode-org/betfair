import datetime
import logging
import time
import typing
from typing import Optional, Generic, TypeVar, List, ClassVar

from .cache import CricketMatchCache, MarketBookCache, OrderBookCache, RaceCache
from ..resources import BaseResource

if typing.TYPE_CHECKING:
    from . import StreamListener

logger = logging.getLogger(__name__)

MAX_CACHE_AGE = 60 * 60 * 8  # 8hrs


T = TypeVar("T", bound=BaseResource)


class BaseStream(Generic[T]):
    """Separate stream class to hold market/order caches"""

    _lookup = "mc"
    _name = "Stream"
    MARKET_ID_FIELD: ClassVar[str]
    IS_IMAGE_FIELD: ClassVar[Optional[str]]

    def __init__(self, listener: "StreamListener", unique_id: int):
        self._listener = listener
        self.unique_id = unique_id
        self.output_queue = listener.output_queue
        self.update_clk = listener.update_clk
        self._max_latency = listener.max_latency
        self._lightweight = listener.lightweight
        self._calculate_market_tv = listener.calculate_market_tv
        self._cumulative_runner_tv = listener.cumulative_runner_tv
        if not hasattr(self, "_updates_only"):
            # set the member if it is not already defined at the class level - only relevant for OrderStream
            self._updates_only = listener.order_updates_only

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
        if self.update_clk:
            self._update_clk(data)

        publish_time = data["pt"]
        if self._max_latency:
            latency = self._calc_latency(publish_time)
            if latency > self._max_latency:
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

    def snap(
        self, market_ids: list = None, publish_time: Optional[int] = None
    ) -> List[T]:
        return [
            cache.create_resource(self.unique_id, snap=True, publish_time=publish_time)
            for cache in list(self._caches.values())
            if cache.active and (market_ids is None or cache.market_id in market_ids)
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
        logger.info('[%s: %s]: "%s" created' % (self, self.unique_id, self))

    def _new_cache_for_update(
        self, market_id: str, publish_time: int, update: dict
    ) -> T:
        """Return a new cache instance for."""
        raise NotImplemented()

    def _process(self, data: list, publish_time: int) -> bool:
        """Return True if new img within data"""
        new_image = False
        caches = []
        for item in data:
            market_id = item[self.MARKET_ID_FIELD]
            is_image = item.get(self.IS_IMAGE_FIELD, False)
            cached_object = self._caches.get(market_id)

            if is_image or cached_object is None:
                new_image = True
                cached_object = self._new_cache_for_update(
                    market_id, publish_time, item
                )
                self._caches[market_id] = cached_object
                logger.info(
                    "[%s: %s]: %s added, %s markets in cache",
                    self,
                    self.unique_id,
                    market_id,
                    len(self._caches),
                )

            cached_object.update_cache(item, publish_time)
            caches.append(cached_object)
            self._updates_processed += 1

        if self._updates_only:
            self.on_process(caches, publish_time)
        else:
            self.on_process(caches)
        return self.IS_IMAGE_FIELD is not None and new_image

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


class MarketStream(BaseStream[MarketBookCache]):
    _updates_only = False
    _lookup = "mc"
    _name = "MarketStream"

    MARKET_ID_FIELD = "id"
    IS_IMAGE_FIELD = "img"

    def _new_cache_for_update(
        self, market_id: str, publish_time: int, update: dict
    ) -> MarketBookCache:
        if "marketDefinition" not in update:
            logger.warning(
                "[%s: %s]: Missing marketDefinition on market %s resulting "
                "in potential missing data in the MarketBook (make sure "
                "EX_MARKET_DEF is requested)" % (self, self.unique_id, market_id)
            )
        return MarketBookCache(
            market_id,
            publish_time,
            self._lightweight,
            self._calculate_market_tv,
            self._cumulative_runner_tv,
        )


class OrderStream(BaseStream[OrderBookCache]):

    _lookup = "oc"
    _name = "OrderStream"

    MARKET_ID_FIELD = "id"
    IS_IMAGE_FIELD = "fullImage"

    def _new_cache_for_update(
        self, market_id: str, publish_time: int, update: dict
    ) -> OrderBookCache:
        return OrderBookCache(market_id, publish_time, self._lightweight)


class RaceStream(BaseStream[RaceCache]):

    """
    Cache contains latest update:
        marketId: RaceCache
    """

    _updates_only = False
    _lookup = "rc"
    _name = "RaceStream"

    MARKET_ID_FIELD = "mid"
    IS_IMAGE_FIELD = None

    def _new_cache_for_update(
        self, market_id: str, publish_time: int, update: dict
    ) -> RaceCache:
        return RaceCache(market_id, publish_time, update.get("id"), self._lightweight)

    def on_subscribe(self, data: dict) -> None:
        """The initial message returned after
        a subscribe - This will currently not
        contain any Race Changes (rc) but may
        do in the future"""
        pass


class CricketStream(BaseStream[CricketMatchCache]):
    _updates_only = False
    _lookup = "cc"
    _name = "CricketStream"

    MARKET_ID_FIELD = "marketId"
    IS_IMAGE_FIELD = None

    def _new_cache_for_update(
        self, market_id: str, publish_time: int, update: dict
    ) -> CricketMatchCache:
        return CricketMatchCache(
            market_id, update["eventId"], publish_time, self._lightweight
        )
