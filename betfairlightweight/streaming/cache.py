from typing import Union

from ..resources import (
    BaseResource,
    MarketBook,
    RunnerBook,
    CurrentOrders,
    MarketDefinition,
    Race,
)
from ..enums import (
    StreamingOrderType,
    StreamingPersistenceType,
    StreamingSide,
    StreamingStatus,
)
from ..utils import create_date_string


class Available:
    """
    Data structure to hold prices/traded amount,
    designed to be as quick as possible.
    """

    __slots__ = [
        "order_book",
        "deletion_select",
        "reverse",
        "serialised",
    ]

    def __init__(self, prices: list, deletion_select: int, reverse: bool = False):
        """
        :param list prices: Current prices
        :param int deletion_select: Used to decide if update should delete cache
        :param bool reverse: Used for sorting
        """
        self.order_book = {}
        self.deletion_select = deletion_select
        self.reverse = reverse
        self.serialised = []
        self.update(prices or [])

    def update(self, book_update: list) -> None:
        deletion_select = self.deletion_select  # local vars
        for book in book_update:
            book = book.copy()  # create copy to keep streaming_update raw
            key = book[0]  # price or position
            if book[deletion_select] == 0:
                # remove price/size
                try:
                    del self.order_book[key]
                except KeyError:
                    continue
            else:
                # serialise once and cache in the book
                book.append(
                    {
                        "price": book[deletion_select - 1],
                        "size": book[deletion_select],
                    }
                )
                if key not in self.order_book:
                    # new price requiring a reorder
                    # to the book.
                    self.order_book[key] = book
                    self._sort_order_book()
                else:
                    # update book
                    self.order_book[key] = book
        self.serialise()

    def clear(self) -> None:
        self.order_book = {}
        self.serialise()

    def serialise(self) -> None:
        self.serialised = [book[-1] for book in self.order_book.values()]

    def _sort_order_book(self) -> None:
        self.order_book = dict(sorted(self.order_book.items(), reverse=self.reverse))


class RunnerBookCache:
    def __init__(
        self,
        id: int,
        lightweight: bool,
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
        definition: dict = None,
    ):
        self.selection_id = id
        self.lightweight = lightweight
        self.last_price_traded = ltp
        self.total_matched = tv
        self.traded = Available(trd, 1)
        self.available_to_back = Available(atb, 1, True)
        self.best_available_to_back = Available(batb, 2)
        self.best_display_available_to_back = Available(bdatb, 2)
        self.available_to_lay = Available(atl, 1)
        self.best_available_to_lay = Available(batl, 2)
        self.best_display_available_to_lay = Available(bdatl, 2)
        self.starting_price_back = Available(spb, 1, True)
        self.starting_price_lay = Available(spl, 1)
        self.starting_price_near = spn
        self.starting_price_far = spf
        self.handicap = hc
        self.definition = definition or {}
        self._definition_status = None
        self._definition_bsp = None
        self._definition_adjustment_factor = None
        self._definition_removal_date = None
        self.update_definition(self.definition)
        self.serialised = {}  # cache is king
        self.resource = None

    def update_definition(self, definition: dict) -> None:
        self.definition = definition
        # cache values used in serialisation to prevent duplicate <get>
        self._definition_status = self.definition.get("status")
        self._definition_bsp = self.definition.get("bsp")
        self._definition_adjustment_factor = self.definition.get("adjustmentFactor")
        self._definition_removal_date = self.definition.get("removalDate")

    def update_traded(self, traded_update: list) -> None:
        """:param traded_update: [price, size]"""
        if not traded_update:
            self.traded.clear()
        else:
            self.traded.update(traded_update)

    def serialise_available_to_back(self) -> list:
        if self.available_to_back.order_book:
            return self.available_to_back.serialised
        elif self.best_display_available_to_back.order_book:
            return self.best_display_available_to_back.serialised
        elif self.best_available_to_back.order_book:
            return self.best_available_to_back.serialised
        else:
            return []

    def serialise_available_to_lay(self) -> list:
        if self.available_to_lay.order_book:
            return self.available_to_lay.serialised
        elif self.best_display_available_to_lay.order_book:
            return self.best_display_available_to_lay.serialised
        elif self.best_available_to_lay.order_book:
            return self.best_available_to_lay.serialised
        return []

    def serialise(self) -> None:
        self.serialised = {
            "status": self._definition_status,
            "ex": {
                "tradedVolume": self.traded.serialised,
                "availableToBack": self.serialise_available_to_back(),
                "availableToLay": self.serialise_available_to_lay(),
            },
            "sp": {
                "nearPrice": self.starting_price_near,
                "farPrice": self.starting_price_far,
                "backStakeTaken": self.starting_price_lay.serialised,
                "layLiabilityTaken": self.starting_price_back.serialised,
                "actualSP": self._definition_bsp,
            },
            "adjustmentFactor": self._definition_adjustment_factor,
            "removalDate": self._definition_removal_date,
            "lastPriceTraded": self.last_price_traded,
            "handicap": self.handicap,
            "totalMatched": self.total_matched,
            "selectionId": self.selection_id,
        }
        if self.lightweight is False:  # cache resource
            self.resource = RunnerBook(**self.serialised)


class MarketBookCache(BaseResource):
    def __init__(self, market_id: str, publish_time: int, lightweight: bool):
        super(MarketBookCache, self).__init__()
        self.market_id = market_id
        self.publish_time = publish_time
        self.lightweight = lightweight
        self.total_matched = None
        self.market_definition = {}
        self._market_definition_resource = None
        self._definition_bet_delay = None
        self._definition_version = None
        self._definition_complete = None
        self._definition_runners_voidable = None
        self._definition_status = None
        self._definition_bsp_reconciled = None
        self._definition_cross_matching = None
        self._definition_in_play = None
        self._definition_number_of_winners = None
        self._definition_number_of_active_runners = None
        self._definition_price_ladder_definition = None
        self._definition_key_line_description = None
        self.streaming_update = None
        self.runners = []
        self.runner_dict = {}
        self._number_of_runners = 0

    def update_cache(self, market_change: dict, publish_time: int) -> None:
        self.streaming_update = market_change
        self.publish_time = publish_time

        if "marketDefinition" in market_change:
            self._process_market_definition(market_change["marketDefinition"])

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
                    runner = self._add_new_runner(**new_data)
                runner.serialise()

    def _process_market_definition(self, market_definition: dict) -> None:
        self.market_definition = market_definition
        if self.lightweight is False:  # cache resource
            self._market_definition_resource = MarketDefinition(**market_definition)
        # cache values used in serialisation to prevent duplicate <get>
        self._definition_bet_delay = market_definition.get("betDelay")
        self._definition_version = market_definition.get("version")
        self._definition_complete = market_definition.get("complete")
        self._definition_runners_voidable = market_definition.get("runnersVoidable")
        self._definition_status = market_definition.get("status")
        self._definition_bsp_reconciled = market_definition.get("bspReconciled")
        self._definition_cross_matching = market_definition.get("crossMatching")
        self._definition_in_play = market_definition.get("inPlay")
        self._definition_number_of_winners = market_definition.get("numberOfWinners")
        self._definition_number_of_active_runners = market_definition.get(
            "numberOfActiveRunners"
        )
        self._definition_price_ladder_definition = market_definition.get(
            "priceLadderDefinition"
        )
        self._definition_key_line_description = market_definition.get(
            "keyLineDefinition"
        )
        # process runners
        for runner_definition in market_definition.get("runners", []):
            selection_id = runner_definition["id"]
            hc = runner_definition.get("hc", 0)
            runner = self.runner_dict.get((selection_id, hc))
            if runner:
                runner.update_definition(runner_definition)
            else:
                runner = self._add_new_runner(
                    id=selection_id, hc=hc, definition=runner_definition
                )
            runner.serialise()

    def _add_new_runner(self, **kwargs) -> RunnerBookCache:
        runner = RunnerBookCache(lightweight=self.lightweight, **kwargs)
        self.runners.append(runner)
        self._number_of_runners = len(self.runners)
        # update runner_dict
        self.runner_dict = {
            (runner.selection_id, runner.handicap): runner for runner in self.runners
        }
        return runner

    def create_resource(
        self, unique_id: int, snap: bool = False
    ) -> Union[dict, MarketBook]:
        data = self.serialise
        data["streaming_unique_id"] = unique_id
        data["streaming_snap"] = snap
        if self.lightweight:
            return data
        else:
            _runners = data.pop("runners", [])
            market_book = MarketBook(
                market_definition=self._market_definition_resource, runners=[], **data
            )
            market_book.runners = [r.resource for r in self.runners]
            market_book._data["runners"] = _runners
            return market_book

    @property
    def closed(self) -> bool:
        if self.market_definition.get("status") == "CLOSED":
            return True
        else:
            return False

    @property
    def serialise(self) -> dict:
        """Creates standard market book json response,
        will contain missing data if EX_MARKET_DEF
        not incl.
        """
        return {
            "marketId": self.market_id,
            "totalAvailable": None,
            "isMarketDataDelayed": None,
            "lastMatchTime": None,
            "betDelay": self._definition_bet_delay,
            "version": self._definition_version,
            "complete": self._definition_complete,
            "runnersVoidable": self._definition_runners_voidable,
            "totalMatched": self.total_matched,
            "status": self._definition_status,
            "bspReconciled": self._definition_bsp_reconciled,
            "crossMatching": self._definition_cross_matching,
            "inplay": self._definition_in_play,
            "numberOfWinners": self._definition_number_of_winners,
            "numberOfRunners": self._number_of_runners,
            "numberOfActiveRunners": self._definition_number_of_active_runners,
            "runners": [runner.serialised for runner in self.runners],
            "publishTime": self.publish_time,
            "priceLadderDefinition": self._definition_price_ladder_definition,
            "keyLineDescription": self._definition_key_line_description,
            "marketDefinition": self.market_definition,  # used in lightweight
            "streaming_update": self.streaming_update,
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
        self.serialised = {}  # cache is king

    def serialise(self, market_id: str, selection_id: int, handicap: int):
        self.serialised = {
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
        market_id: str,
        id: int,
        fullImage: dict = None,
        ml: list = None,
        mb: list = None,
        uo: list = None,
        hc: int = 0,
        smc: dict = None,
    ):
        self.market_id = market_id
        self.selection_id = id
        self.full_image = fullImage
        self.matched_lays = Available(ml, 1)
        self.matched_backs = Available(mb, 1)
        self.unmatched_orders = {}  # {betId: UnmatchedOrder..
        self.handicap = hc
        self.strategy_matches = smc
        self.update_unmatched(uo or [])

    def update_unmatched(self, unmatched_orders: list) -> None:
        for unmatched_order in unmatched_orders:
            order = UnmatchedOrder(**unmatched_order)
            order.serialise(self.market_id, self.selection_id, self.handicap)
            self.unmatched_orders[order.bet_id] = order

    def serialise_orders(self) -> list:
        orders = list(self.unmatched_orders.values())  # order may be added (#232)
        return [order.serialised for order in orders]

    def serialise_matches(self) -> dict:
        return {
            "selectionId": self.selection_id,
            "matchedLays": self.matched_lays.serialised,
            "matchedBacks": self.matched_backs.serialised,
        }


class OrderBookCache(BaseResource):
    def __init__(self, market_id: str, publish_time: int, lightweight: bool):
        super(OrderBookCache, self).__init__()
        self.market_id = market_id
        self.publish_time = publish_time
        self.lightweight = lightweight
        self.closed = None
        self.streaming_update = None
        self.runners = {}  # (selectionId, handicap):

    def update_cache(self, order_book: dict, publish_time: int) -> None:
        self.streaming_update = order_book
        self.publish_time = publish_time
        if "closed" in order_book:
            self.closed = order_book["closed"]

        for order_changes in order_book.get("orc", []):
            selection_id = order_changes["id"]
            handicap = order_changes.get("hc", 0)
            full_image = order_changes.get("fullImage")
            _lookup = (selection_id, handicap)
            runner = self.runners.get(_lookup)
            if full_image or runner is None:
                self.runners[_lookup] = OrderBookRunner(self.market_id, **order_changes)
            else:
                if "ml" in order_changes:
                    runner.matched_lays.update(order_changes["ml"])
                if "mb" in order_changes:
                    runner.matched_backs.update(order_changes["mb"])
                if "uo" in order_changes:
                    runner.update_unmatched(order_changes["uo"])

    def create_resource(
        self, unique_id: int, snap: bool = False
    ) -> Union[dict, CurrentOrders]:
        data = self.serialise
        data["streaming_unique_id"] = unique_id
        data["streaming_snap"] = snap
        if self.lightweight:
            return data
        else:
            return CurrentOrders(publish_time=self.publish_time, **data)

    @property
    def serialise(self) -> dict:
        runners = list(self.runners.values())  # runner may be added
        orders, matches = [], []
        for runner in runners:
            orders.extend(runner.serialise_orders())
            matches.append(runner.serialise_matches())
        return {
            "currentOrders": orders,
            "matches": matches,
            "moreAvailable": False,
            "streaming_update": self.streaming_update,
        }


class RaceCache(BaseResource):
    def __init__(
        self, market_id: str, publish_time: int, race_id: str, lightweight: bool
    ):
        super(RaceCache, self).__init__()
        self.market_id = market_id
        self.publish_time = publish_time
        self.race_id = race_id
        self.lightweight = lightweight
        self.rpc = None  # RaceProgressChange
        self.rrc = {}  # {id: RaceRunnerChange..
        self.streaming_update = None

    def update_cache(self, update: dict, publish_time: int) -> None:
        self.streaming_update = update
        self.publish_time = publish_time

        if "rpc" in update:
            self.rpc = update["rpc"]

        if "rrc" in update:
            for runner_update in update["rrc"]:
                self.rrc[runner_update["id"]] = runner_update

    def create_resource(self, unique_id: int, snap: bool = False) -> Union[dict, Race]:
        data = self.serialise
        data["streaming_unique_id"] = unique_id
        data["streaming_snap"] = snap
        if self.lightweight:
            return data
        else:
            return Race(**data)

    @property
    def serialise(self) -> dict:
        return {
            "pt": self.publish_time,
            "mid": self.market_id,
            "id": self.race_id,
            "rpc": self.rpc,
            "rrc": list(self.rrc.values()),
            "streaming_update": self.streaming_update,
        }
