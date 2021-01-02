import datetime
from typing import Union

from ..resources import BaseResource, MarketBook, CurrentOrders, MarketDefinition, Race
from ..enums import (
    StreamingOrderType,
    StreamingPersistenceType,
    StreamingSide,
    StreamingStatus,
)
from ..exceptions import CacheError
from ..utils import create_date_string
from ._cache import *


class RunnerBook:
    def __init__(
        self,
        id: int,
        ltp: float = None,
        tv: float = None,
        trd: list = None,
        atb: list = None,
        batb: list = None,
        bdatb: list = None,
        atl: list = None,
        batl: list = None,
        bdatl: list = None,
        spn: float = None,
        spf: float = None,
        spb: list = None,
        spl: list = None,
        hc: int = 0,
    ):
        self.selection_id = id
        self.last_price_traded = ltp
        self.total_matched = tv
        self.traded = Available(trd, 1)
        self.available_to_back = Available(atb, 1, True)
        self.best_available_to_back = Available(batb, 2)
        self.best_display_available_to_back = Available(bdatb, 2)
        self.available_to_lay = Available(atl, 1)
        self.best_available_to_lay = Available(batl, 2)
        self.best_display_available_to_lay = Available(bdatl, 2)
        self.starting_price_back = Available(spb, 1)
        self.starting_price_lay = Available(spl, 1)
        self.starting_price_near = spn
        self.starting_price_far = spf
        self.handicap = hc

    def update_traded(self, traded_update: list) -> None:
        """:param traded_update: [price, size]"""
        if not traded_update:
            self.traded.clear()
        else:
            self.traded.update(traded_update)

    def serialise_available_to_back(self) -> list:
        if self.available_to_back.prices:
            return self.available_to_back.serialise
        elif self.best_display_available_to_back.prices:
            return self.best_display_available_to_back.serialise
        elif self.best_available_to_back.prices:
            return self.best_available_to_back.serialise
        else:
            return []

    def serialise_available_to_lay(self) -> list:
        if self.available_to_lay.prices:
            return self.available_to_lay.serialise
        elif self.best_display_available_to_lay.prices:
            return self.best_display_available_to_lay.serialise
        elif self.best_available_to_lay.prices:
            return self.best_available_to_lay.serialise
        return []

    def serialise(self, runner_definition: dict) -> dict:
        return {
            "status": runner_definition.get("status"),
            "ex": {
                "tradedVolume": self.traded.serialise,
                "availableToBack": self.serialise_available_to_back(),
                "availableToLay": self.serialise_available_to_lay(),
            },
            "sp": {
                "nearPrice": self.starting_price_near,
                "farPrice": self.starting_price_far,
                "backStakeTaken": self.starting_price_back.serialise,
                "layLiabilityTaken": self.starting_price_lay.serialise,
                "actualSP": runner_definition.get("bsp"),
            },
            "adjustmentFactor": runner_definition.get("adjustmentFactor"),
            "removalDate": runner_definition.get("removalDate"),
            "lastPriceTraded": self.last_price_traded,
            "handicap": self.handicap,
            "totalMatched": self.total_matched,
            "selectionId": self.selection_id,
        }


class MarketBookCache(BaseResource):
    def __init__(self, **kwargs):
        super(MarketBookCache, self).__init__(**kwargs)
        self.publish_time = kwargs.get("publish_time")
        self.market_id = kwargs.get("id")
        self.image = kwargs.get("img")
        self.total_matched = kwargs.get("tv")
        if "marketDefinition" not in kwargs:
            raise CacheError('"EX_MARKET_DEF" must be requested to use cache')
        self.market_definition = kwargs["marketDefinition"]

        self.streaming_update = None
        self.runners = []
        self.runner_dict = {}
        self.market_definition_runner_dict = {}
        self._update_runner_dict()
        self._update_market_definition_runner_dict()

    def update_cache(self, market_change: dict, publish_time: int) -> None:
        self._datetime_updated = (
            self.strip_datetime(publish_time) or self._datetime_updated
        )
        self.publish_time = publish_time
        self.streaming_update = market_change

        if "marketDefinition" in market_change:
            self.market_definition = market_change["marketDefinition"]
            self._update_market_definition_runner_dict()

        if "tv" in market_change:
            self.total_matched = market_change["tv"]

        if "rc" in market_change:
            for new_data in market_change["rc"]:
                runner = self.runner_dict.get((new_data["id"], new_data.get("hc", 0)))
                if runner:
                    if "ltp" in new_data:
                        runner.last_price_traded = new_data["ltp"]
                    if "tv" in new_data:  # if runner removed tv: 0 is returned
                        runner.total_matched = new_data["tv"]
                    if "spn" in new_data:
                        runner.starting_price_near = new_data["spn"]
                    if "spf" in new_data:
                        runner.starting_price_far = new_data["spf"]
                    if "trd" in new_data:
                        runner.update_traded(new_data["trd"])
                    if "atb" in new_data:
                        runner.available_to_back.update(new_data["atb"])
                    if "atl" in new_data:
                        runner.available_to_lay.update(new_data["atl"])
                    if "batb" in new_data:
                        runner.best_available_to_back.update(new_data["batb"])
                    if "batl" in new_data:
                        runner.best_available_to_lay.update(new_data["batl"])
                    if "bdatb" in new_data:
                        runner.best_display_available_to_back.update(new_data["bdatb"])
                    if "bdatl" in new_data:
                        runner.best_display_available_to_lay.update(new_data["bdatl"])
                    if "spb" in new_data:
                        runner.starting_price_back.update(new_data["spb"])
                    if "spl" in new_data:
                        runner.starting_price_lay.update(new_data["spl"])
                else:
                    self.runners.append(RunnerBook(**new_data))
                    self._update_runner_dict()

    def create_resource(
        self, unique_id: int, lightweight: bool, snap: bool = False
    ) -> Union[dict, MarketBook]:
        data = self.serialise
        data["streaming_unique_id"] = unique_id
        data["streaming_update"] = self.streaming_update
        data["streaming_snap"] = snap
        if lightweight:
            return data
        else:
            return MarketBook(
                elapsed_time=(
                    datetime.datetime.utcnow() - self._datetime_updated
                ).total_seconds(),
                market_definition=MarketDefinition(**self.market_definition),
                **data
            )

    def _update_runner_dict(self) -> None:
        self.runner_dict = {
            (runner.selection_id, runner.handicap): runner for runner in self.runners
        }

    def _update_market_definition_runner_dict(self) -> None:
        self.market_definition_runner_dict = {
            (runner["id"], runner.get("hc", 0)): runner
            for runner in self.market_definition["runners"]
        }

    @property
    def closed(self) -> bool:
        if self.market_definition.get("status") == "CLOSED":
            return True
        else:
            return False

    @property
    def serialise(self) -> dict:
        """Creates standard market book json response,
        will error if EX_MARKET_DEF not incl.
        """
        return {
            "marketId": self.market_id,
            "totalAvailable": None,
            "isMarketDataDelayed": None,
            "lastMatchTime": None,
            "betDelay": self.market_definition.get("betDelay"),
            "version": self.market_definition.get("version"),
            "complete": self.market_definition.get("complete"),
            "runnersVoidable": self.market_definition.get("runnersVoidable"),
            "totalMatched": self.total_matched,
            "status": self.market_definition.get("status"),
            "bspReconciled": self.market_definition.get("bspReconciled"),
            "crossMatching": self.market_definition.get("crossMatching"),
            "inplay": self.market_definition.get("inPlay"),
            "numberOfWinners": self.market_definition.get("numberOfWinners"),
            "numberOfRunners": len(self.market_definition.get("runners")),
            "numberOfActiveRunners": self.market_definition.get(
                "numberOfActiveRunners"
            ),
            "runners": [
                runner.serialise(
                    self.market_definition_runner_dict[
                        (runner.selection_id, runner.handicap)
                    ]
                )
                for runner in self.runners
            ],
            "publishTime": self.publish_time,
            "priceLadderDefinition": self.market_definition.get(
                "priceLadderDefinition"
            ),
            "keyLineDescription": self.market_definition.get("keyLineDefinition"),
            "marketDefinition": self.market_definition,  # used in lightweight
        }


class UnmatchedOrder:
    def __init__(
        self,
        id: str,
        p: float,
        s: float,
        side: str,
        status: str,
        ot: str,
        pd: int,
        sm: float,
        sr: float,
        sl: float,
        sc: float,
        sv: float,
        rfo: str,
        rfs: str,
        pt: str = None,
        md: str = None,
        avp: float = None,
        bsp: float = None,
        ld: int = None,
        rac: str = None,
        rc: str = None,
        lsrc: str = None,
        cd: int = None,
        **kwargs
    ):
        self.bet_id = id
        self.price = p
        self.size = s
        self.bsp_liability = bsp
        self.side = side
        self.status = status
        self.persistence_type = pt
        self.order_type = ot
        self.placed_date = BaseResource.strip_datetime(pd)
        self._placed_date_string = create_date_string(self.placed_date)
        self.matched_date = BaseResource.strip_datetime(md)
        self._matched_date_string = create_date_string(self.matched_date)
        self.average_price_matched = avp
        self.size_matched = sm
        self.size_remaining = sr
        self.size_lapsed = sl
        self.size_cancelled = sc
        self.size_voided = sv
        self.regulator_auth_code = rac
        self.regulator_code = rc
        self.reference_order = rfo
        self.reference_strategy = rfs
        self.lapsed_date = BaseResource.strip_datetime(ld)
        self._lapsed_date_string = create_date_string(self.lapsed_date)
        self.lapse_status_reason_code = lsrc
        self.cancelled_date = BaseResource.strip_datetime(cd)
        self._cancelled_date_string = create_date_string(self.cancelled_date)

    def serialise(self, market_id: str, selection_id: int, handicap: int) -> dict:
        return {
            "averagePriceMatched": self.average_price_matched or 0.0,
            "betId": self.bet_id,
            "bspLiability": self.bsp_liability,
            "handicap": handicap,
            "marketId": market_id,
            "matchedDate": self._matched_date_string,
            "orderType": StreamingOrderType[self.order_type].value,
            "persistenceType": StreamingPersistenceType[self.persistence_type].value
            if self.persistence_type
            else None,
            "placedDate": self._placed_date_string,
            "priceSize": {"price": self.price, "size": self.size},
            "regulatorAuthCode": self.regulator_auth_code,
            "regulatorCode": self.regulator_code,
            "selectionId": selection_id,
            "side": StreamingSide[self.side].value,
            "sizeCancelled": self.size_cancelled,
            "sizeLapsed": self.size_lapsed,
            "sizeMatched": self.size_matched,
            "sizeRemaining": self.size_remaining,
            "sizeVoided": self.size_voided,
            "status": StreamingStatus[self.status].value,
            "customerStrategyRef": self.reference_strategy,
            "customerOrderRef": self.reference_order,
            "lapsedDate": self._lapsed_date_string,
            "lapseStatusReasonCode": self.lapse_status_reason_code,
            "cancelledDate": self._cancelled_date_string,
        }


class OrderBookRunner:
    def __init__(
        self,
        id: int,
        fullImage: dict = None,
        ml: list = None,
        mb: list = None,
        uo: list = None,
        hc: int = 0,
        smc: dict = None,
    ):
        self.selection_id = id
        self.full_image = fullImage
        self.matched_lays = Available(ml, 1)
        self.matched_backs = Available(mb, 1)
        self.unmatched_orders = {i["id"]: UnmatchedOrder(**i) for i in uo} if uo else {}
        self.handicap = hc
        self.strategy_matches = smc

    def update_unmatched(self, unmatched_orders: list) -> None:
        for unmatched_order in unmatched_orders:
            self.unmatched_orders[unmatched_order["id"]] = UnmatchedOrder(
                **unmatched_order
            )

    def serialise_orders(self, market_id: str) -> list:
        orders = list(self.unmatched_orders.values())  # order may be added (#232)
        return [
            order.serialise(market_id, self.selection_id, self.handicap)
            for order in orders
        ]


class OrderBookCache(BaseResource):
    def __init__(self, **kwargs):
        super(OrderBookCache, self).__init__(**kwargs)
        self.publish_time = kwargs.get("publish_time")
        self.market_id = kwargs.get("id")
        self.closed = kwargs.get("closed")
        self.streaming_update = None
        self.runners = {}  # (selectionId, handicap):

    def update_cache(self, order_book: dict, publish_time: int) -> None:
        self._datetime_updated = self.strip_datetime(publish_time)
        self.publish_time = publish_time
        self.streaming_update = order_book
        if "closed" in order_book:
            self.closed = order_book["closed"]

        for order_changes in order_book.get("orc", []):
            selection_id = order_changes["id"]
            handicap = order_changes.get("hc", 0)
            full_image = order_changes.get("fullImage")
            _lookup = (selection_id, handicap)
            runner = self.runners.get(_lookup)
            if full_image or runner is None:
                self.runners[_lookup] = OrderBookRunner(**order_changes)
            else:
                if "ml" in order_changes:
                    runner.matched_lays.update(order_changes["ml"])
                if "mb" in order_changes:
                    runner.matched_backs.update(order_changes["mb"])
                if "uo" in order_changes:
                    runner.update_unmatched(order_changes["uo"])

    def create_resource(
        self, unique_id: int, lightweight: bool, snap: bool = False
    ) -> Union[dict, CurrentOrders]:
        data = self.serialise
        data["streaming_unique_id"] = unique_id
        data["streaming_update"] = self.streaming_update
        data["streaming_snap"] = snap
        if lightweight:
            return data
        else:
            return CurrentOrders(
                elapsed_time=(
                    datetime.datetime.utcnow() - self._datetime_updated
                ).total_seconds(),
                publish_time=self.publish_time,
                **data
            )

    @property
    def serialise(self) -> dict:
        runners = list(self.runners.values())  # runner may be added
        orders = []
        for runner in runners:
            orders.extend(runner.serialise_orders(self.market_id))
        return {"currentOrders": orders, "moreAvailable": False}


class RunnerChange:
    def __init__(self, change: dict):
        self.change = change


class RaceCache(BaseResource):
    def __init__(self, **kwargs):
        super(RaceCache, self).__init__(**kwargs)
        self.publish_time = kwargs.get("publish_time")
        self.market_id = kwargs.get("mid")
        self.race_id = kwargs.get("id")
        self.rpc = kwargs.get("rpc")  # RaceProgressChange
        self.rrc = [RunnerChange(i) for i in kwargs.get("rrc", [])]  # RaceRunnerChange
        self.streaming_update = None

    def update_cache(self, update: dict, publish_time: int) -> None:
        self._datetime_updated = self.strip_datetime(publish_time)
        self.publish_time = publish_time
        self.streaming_update = update

        if "rpc" in update:
            self.rpc = update["rpc"]

        if "rrc" in update:
            runner_dict = {runner.change["id"]: runner for runner in self.rrc}

            for runner_update in update["rrc"]:
                runner = runner_dict.get(runner_update["id"])
                if runner:
                    runner.change = runner_update
                else:
                    self.rrc.append(RunnerChange(runner_update))

    def create_resource(
        self, unique_id: int, lightweight: bool, snap: bool = False
    ) -> Union[dict, Race]:
        data = self.serialise
        data["streaming_unique_id"] = unique_id
        data["streaming_update"] = self.streaming_update
        data["streaming_snap"] = snap
        if lightweight:
            return data
        else:
            return Race(
                elapsed_time=(
                    datetime.datetime.utcnow() - self._datetime_updated
                ).total_seconds(),
                **data
            )

    @property
    def serialise(self) -> dict:
        return {
            "pt": self.publish_time,
            "mid": self.market_id,
            "id": self.race_id,
            "rpc": self.rpc,
            "rrc": [runner.change for runner in self.rrc],
        }
