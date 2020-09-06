import datetime
from typing import Union

from ..resources import (
    BaseResource,
    MarketBook,
    CurrentOrders,
    MarketDefinition,
    MarketDefinitionRunner,
    PriceSize,
    PriceSizeList,
    PositionPriceSize,
    PositionPriceSizeList,
)
from ..enums import (
    StreamingOrderType,
    StreamingPersistenceType,
    StreamingSide,
    StreamingStatus,
)
from ..exceptions import CacheError


class Available:
    """
    Data structure to hold prices/traded amount,
    designed to be as quick as possible.
    """

    def __init__(self, prices: list, deletion_select: int, reverse: bool = False):
        """
        :param list prices: Current prices
        :param int deletion_select: Used to decide if update should delete cache
        :param bool reverse: Used for sorting
        """
        self.prices = prices or []
        self.deletion_select = deletion_select
        self.reverse = reverse

        self.serialise = []
        self.sort()

    def sort(self) -> None:
        self.prices.sort(reverse=self.reverse)
        self.serialise = [
            PriceSize(
                price=volume[self.deletion_select - 1],
                size=volume[self.deletion_select],
            )
            for volume in self.prices
        ]

    def clear(self) -> None:
        self.prices = []
        self.sort()

    def update(self, book_update: list) -> None:
        for book in book_update:
            for (count, trade) in enumerate(self.prices):
                if trade[0] == book[0]:
                    if book[self.deletion_select] == 0:
                        del self.prices[count]
                        break
                    else:
                        self.prices[count] = book
                        break
            else:
                if book[self.deletion_select] != 0:
                    # handles betfair bug,
                    # https://forum.developer.betfair.com/forum/sports-exchange-api/exchange-api/3425-streaming-bug
                    self.prices.append(book)
        self.sort()


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
        self.traded = PriceSizeList(trd)
        self.available_to_back = PriceSizeList(atb, reverse=True)
        self.best_available_to_back = PositionPriceSizeList(batb)
        self.best_display_available_to_back = PositionPriceSizeList(bdatb)
        self.available_to_lay = Available(atl, 1)
        self.best_available_to_lay = Available(batl, 2)
        self.best_display_available_to_lay = Available(bdatl, 2)
        self.starting_price_back = PriceSizeList(spb)
        self.starting_price_lay = PriceSizeList(spl)
        self.starting_price_near = spn
        self.starting_price_far = spf
        self.handicap = hc

    def update_traded(self, traded_update: list) -> None:
        """:param traded_update: [price, size]"""
        if not traded_update:
            self.traded.clear()
        else:
            self.traded.update(traded_update)

    def serialise_available_to_back(
        self,
    ) -> Union[PriceSizeList, PositionPriceSizeList]:
        if self.available_to_back:
            return self.available_to_back
        elif self.best_display_available_to_back:
            return self.best_display_available_to_back
        elif self.best_available_to_back:
            return self.best_available_to_back
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

    def serialise(self, runner_definition: MarketDefinitionRunner) -> dict:
        return {
            "status": runner_definition.status,
            "ex": {
                "tradedVolume": self.traded,
                "availableToBack": self.serialise_available_to_back(),
                "availableToLay": self.serialise_available_to_lay(),
            },
            "sp": {
                "nearPrice": self.starting_price_near,
                "farPrice": self.starting_price_far,
                "backStakeTaken": self.starting_price_back,
                "layLiabilityTaken": self.starting_price_lay,
                "actualSP": runner_definition.bsp,
            },
            "adjustmentFactor": runner_definition.adjustment_factor,
            "removalDate": runner_definition.removal_date,
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
        self.parsed_market_definition = MarketDefinition(**self.market_definition)

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
            self.parsed_market_definition = MarketDefinition(**self.market_definition)
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
        self, unique_id: int, lightweight: bool
    ) -> Union[dict, MarketBook]:
        data = self.serialise
        data["streaming_unique_id"] = unique_id
        data["streaming_update"] = self.streaming_update
        if lightweight:
            return data
        else:
            return MarketBook(
                elapsed_time=(
                    datetime.datetime.utcnow() - self._datetime_updated
                ).total_seconds(),
                market_definition=self.parsed_market_definition,
                **data
            )

    def _update_runner_dict(self) -> None:
        self.runner_dict = {
            (runner.selection_id, runner.handicap): runner for runner in self.runners
        }

    def _update_market_definition_runner_dict(self) -> None:
        self.market_definition_runner_dict = {
            (runner.selection_id, runner.handicap): runner
            for runner in self.parsed_market_definition.runners
        }

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
            "betDelay": self.parsed_market_definition.bet_delay,
            "version": self.parsed_market_definition.version,
            "complete": self.parsed_market_definition.complete,
            "runnersVoidable": self.parsed_market_definition.runners_voidable,
            "totalMatched": self.total_matched,
            "status": self.parsed_market_definition.status,
            "bspReconciled": self.parsed_market_definition.bsp_reconciled,
            "crossMatching": self.parsed_market_definition.cross_matching,
            "inplay": self.parsed_market_definition.in_play,
            "numberOfWinners": self.parsed_market_definition.number_of_winners,
            "numberOfRunners": len(self.parsed_market_definition.runners),
            "numberOfActiveRunners": self.parsed_market_definition.number_of_active_runners,
            "runners": [
                runner.serialise(
                    self.market_definition_runner_dict[
                        (runner.selection_id, runner.handicap)
                    ]
                )
                for runner in self.runners
            ],
            "publishTime": self.publish_time,
            "priceLadderDefinition": self.parsed_market_definition.price_ladder_definition,
            "keyLineDescription": self.parsed_market_definition.key_line_definitions,
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
        self.placed_date_string = self.create_placed_date_string()
        self.matched_date = BaseResource.strip_datetime(md)
        self.matched_date_string = self.create_matched_date_string()
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
        self.lapse_status_reason_code = lsrc  # todo add to output?

    def create_placed_date_string(self) -> str:
        if self.placed_date:
            return self.placed_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def create_matched_date_string(self) -> str:
        if self.matched_date:
            return self.matched_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def serialise(self, market_id: str, selection_id: int, handicap: int) -> dict:
        return {
            "averagePriceMatched": self.average_price_matched or 0.0,
            "betId": self.bet_id,
            "bspLiability": self.bsp_liability,
            "handicap": handicap,
            "marketId": market_id,
            "matchedDate": self.matched_date_string,
            "orderType": StreamingOrderType[self.order_type].value,
            "persistenceType": StreamingPersistenceType[self.persistence_type].value
            if self.persistence_type
            else None,
            "placedDate": self.placed_date_string,
            "priceSize": {"price": self.price, "size": self.size},
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
        # order may be added (#232)
        orders = list(self.unmatched_orders.values())
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
        self.runners = []

    def update_cache(self, order_book: dict, publish_time: int) -> None:
        self._datetime_updated = self.strip_datetime(publish_time)
        self.publish_time = publish_time
        self.streaming_update = order_book
        if "closed" in order_book:
            self.closed = order_book["closed"]

        for order_changes in order_book.get("orc", []):
            selection_id = order_changes["id"]
            handicap = order_changes.get("hc", 0)
            runner = self.runner_dict.get((selection_id, handicap))
            if runner:
                if "ml" in order_changes:
                    runner.matched_lays.update(order_changes["ml"])
                if "mb" in order_changes:
                    runner.matched_backs.update(order_changes["mb"])
                if "uo" in order_changes:
                    runner.update_unmatched(order_changes["uo"])
            else:
                self.runners.append(OrderBookRunner(**order_changes))

    def create_resource(
        self, unique_id: int, lightweight: bool
    ) -> Union[dict, CurrentOrders]:
        data = self.serialise
        data["streaming_unique_id"] = unique_id
        data["streaming_update"] = self.streaming_update
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
    def runner_dict(self) -> dict:
        return {
            (runner.selection_id, runner.handicap): runner for runner in self.runners
        }

    @property
    def serialise(self) -> dict:
        orders = []
        for runner in self.runners:
            orders.extend(runner.serialise_orders(self.market_id))
        return {"currentOrders": orders, "moreAvailable": False}
