from .baseresource import BaseResource


class EventType:
    """
    :type id: unicode
    :type name: unicode
    """

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name


class EventTypeResult(BaseResource):
    """
    :type event_type: EventType
    :type market_count: int
    """

    def __init__(self, **kwargs):
        super(EventTypeResult, self).__init__(**kwargs)
        self.market_count = kwargs.get("marketCount")
        self.event_type = EventType(**kwargs.get("eventType"))


class Competition:
    """
    :type id: unicode
    :type name: unicode
    """

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name


class CompetitionResult(BaseResource):
    """
    :type competition: Competition
    :type competition_region: unicode
    :type market_count: int
    """

    def __init__(self, **kwargs):
        super(CompetitionResult, self).__init__(**kwargs)
        self.market_count = kwargs.get("marketCount")
        self.competition_region = kwargs.get("competitionRegion")
        self.competition = Competition(**kwargs.get("competition"))


class TimeRange:
    """
    :type _from: datetime.datetime
    :type to: datetime.datetime
    """

    def __init__(self, **kwargs):
        self._from = BaseResource.strip_datetime(kwargs.get("from"))
        self.to = BaseResource.strip_datetime(kwargs.get("to"))


class TimeRangeResult(BaseResource):
    """
    :type market_count: int
    :type time_range: TimeRange
    """

    def __init__(self, **kwargs):
        super(TimeRangeResult, self).__init__(**kwargs)
        self.market_count = kwargs.get("marketCount")
        self.time_range = TimeRange(**kwargs.get("timeRange"))


class Event:
    """
    :type country_code: unicode
    :type id: unicode
    :type name: unicode
    :type open_date: datetime.datetime
    :type time_zone: unicode
    :type venue: unicode
    """

    def __init__(
        self,
        id: str,
        openDate: str,
        timezone: str,
        name: str,
        countryCode: str = None,
        venue: str = None,
    ):
        self.id = id
        self.open_date = BaseResource.strip_datetime(openDate)
        self.time_zone = timezone
        self.country_code = countryCode
        self.name = name
        self.venue = venue


class EventResult(BaseResource):
    """
    :type event: Event
    :type market_count: int
    """

    def __init__(self, **kwargs):
        super(EventResult, self).__init__(**kwargs)
        self.market_count = kwargs.get("marketCount")
        self.event = Event(**kwargs.get("event"))


class MarketTypeResult(BaseResource):
    """
    :type market_count: int
    :type market_type: unicode
    """

    def __init__(self, **kwargs):
        super(MarketTypeResult, self).__init__(**kwargs)
        self.market_count = kwargs.get("marketCount")
        self.market_type = kwargs.get("marketType")


class CountryResult(BaseResource):
    """
    :type country_code: unicode
    :type market_count: int
    """

    def __init__(self, **kwargs):
        super(CountryResult, self).__init__(**kwargs)
        self.market_count = kwargs.get("marketCount")
        self.country_code = kwargs.get("countryCode")


class VenueResult(BaseResource):
    """
    :type market_count: int
    :type venue: unicode
    """

    def __init__(self, **kwargs):
        super(VenueResult, self).__init__(**kwargs)
        self.market_count = kwargs.get("marketCount")
        self.venue = kwargs.get("venue")


class LineRangeInfo:
    """
    :type marketUnit: unicode
    :type interval: float
    :type minUnitValue: float
    :type maxUnitValue: float
    """

    def __init__(
        self, marketUnit: str, interval: float, minUnitValue: float, maxUnitValue: float
    ):
        self.market_unit = marketUnit
        self.interval = interval
        self.min_unit_value = minUnitValue
        self.max_unit_value = maxUnitValue


class PriceLadderDescription:
    """
    :type type: unicode
    """

    def __init__(self, type: str):
        self.type = type

    def serialise(self):
        return {"type": self.type}


class MarketCatalogueDescription:
    """
    :type betting_type: unicode
    :type bsp_market: bool
    :type clarifications: unicode
    :type discount_allowed: bool
    :type each_way_divisor: float
    :type market_base_rate: float
    :type market_time: datetime.datetime
    :type market_type: unicode
    :type persistence_enabled: bool
    :type regulator: unicode
    :type rules: unicode
    :type rules_has_date: bool
    :type suspend_time: datetime.datetime
    :type turn_in_play_enabled: bool
    :type wallet: unicode
    """

    def __init__(
        self,
        bettingType: str,
        bspMarket: bool,
        marketTime: str,
        suspendTime: str,
        turnInPlayEnabled: bool,
        wallet: str = None,
        marketType: str = None,
        discountAllowed: bool = None,
        marketBaseRate: float = None,
        persistenceEnabled: bool = None,
        regulator: str = None,
        rules: str = None,
        rulesHasDate: bool = None,
        eachWayDivisor: float = None,
        clarifications: str = None,
        priceLadderDescription: dict = None,
        keyLineDefinition: str = None,
        lineRangeInfo: dict = None,
        raceType: str = None,
    ):
        self.betting_type = bettingType
        self.bsp_market = bspMarket
        self.discount_allowed = discountAllowed
        self.market_base_rate = marketBaseRate
        self.market_time = BaseResource.strip_datetime(marketTime)
        self.market_type = marketType
        self.persistence_enabled = persistenceEnabled
        self.regulator = regulator
        self.rules = rules
        self.rules_has_date = rulesHasDate
        self.suspend_time = BaseResource.strip_datetime(suspendTime)
        self.turn_in_play_enabled = turnInPlayEnabled
        self.wallet = wallet
        self.each_way_divisor = eachWayDivisor
        self.clarifications = clarifications
        self.price_ladder_description = (
            PriceLadderDescription(**priceLadderDescription)
            if priceLadderDescription
            else None
        )
        self.line_range_info = LineRangeInfo(**lineRangeInfo) if lineRangeInfo else None
        self.race_type = raceType


class RunnerCatalogue:
    """
    :type handicap: float
    :type metadata: dict
    :type runner_name: unicode
    :type selection_id: int
    :type sort_priority: int
    """

    def __init__(self, **kwargs):
        self.selection_id = kwargs.get("selectionId")
        self.runner_name = kwargs.get("runnerName")
        self.sort_priority = kwargs.get("sortPriority")
        self.handicap = kwargs.get("handicap")
        self.metadata = kwargs.get("metadata")

    def __str__(self):
        return "RunnerCatalogue: %s" % self.selection_id

    def __repr__(self):
        return "<RunnerCatalogue>"


class MarketCatalogue(BaseResource):
    """
    :type competition: Competition
    :type description: MarketCatalogueDescription
    :type event: Event
    :type event_type: EventType
    :type market_id: unicode
    :type market_name: unicode
    :type market_start_time: datetime.datetime
    :type runners: list[RunnerCatalogue]
    :type total_matched: float
    """

    def __init__(self, **kwargs):
        super(MarketCatalogue, self).__init__(**kwargs)
        self.market_id = kwargs.get("marketId")
        self.market_name = kwargs.get("marketName")
        self.total_matched = kwargs.get("totalMatched")
        self.market_start_time = self.strip_datetime(kwargs.get("marketStartTime"))
        self.competition = (
            Competition(**kwargs.get("competition"))
            if kwargs.get("competition")
            else None
        )
        self.event = Event(**kwargs.get("event")) if kwargs.get("event") else None
        self.event_type = (
            EventType(**kwargs.get("eventType")) if kwargs.get("eventType") else None
        )
        self.description = (
            MarketCatalogueDescription(**kwargs.get("description"))
            if kwargs.get("description")
            else None
        )
        self.runners = [RunnerCatalogue(**i) for i in kwargs.get("runners", [])]


"""
__slots__ is a terrible hack with nasty, hard-to-fathom side
effects that should only be used by programmers at grandmaster and
wizard levels. Unfortunately it has gained an enormous undeserved
popularity amongst the novices and apprentices, who should know
better than to use this magic incantation casually.
"""


class Slotable:
    __slots__ = []

    def __getstate__(self):
        return {slot: getattr(self, slot) for slot in self.__slots__}

    def __setstate__(self, d):
        for slot in d:
            setattr(self, slot, d[slot])


class PriceSize(Slotable):
    """
    :type price: float
    :type size: float
    """

    __slots__ = ["price", "size"]

    def __init__(self, price: float, size: float):
        self.price = price
        self.size = size

    def __str__(self):
        return "Price: %s Size: %s" % (self.price, self.size)


class RunnerBookSP:
    """
    :type actual_sp: float
    :type back_stake_taken: list[PriceSize]
    :type far_price: float
    :type lay_liability_taken: list[PriceSize]
    :type near_price: float
    """

    def __init__(
        self,
        nearPrice: float = None,
        farPrice: float = None,
        backStakeTaken: list = None,
        layLiabilityTaken: list = None,
        actualSP: float = None,
    ):
        self.near_price = nearPrice
        self.far_price = farPrice
        self.actual_sp = actualSP
        self.back_stake_taken = [PriceSize(**i) for i in backStakeTaken]
        self.lay_liability_taken = [PriceSize(**i) for i in layLiabilityTaken]


class RunnerBookEX:
    """
    :type available_to_back: list[PriceSize]
    :type available_to_lay: list[PriceSize]
    :type traded_volume: list[PriceSize]
    """

    def __init__(
        self,
        availableToBack: list = None,
        availableToLay: list = None,
        tradedVolume: list = None,
    ):
        self.available_to_back = [PriceSize(**i) for i in availableToBack]
        self.available_to_lay = [PriceSize(**i) for i in availableToLay]
        self.traded_volume = [PriceSize(**i) for i in tradedVolume]


class RunnerBookOrder:
    """
    :type avg_price_matched: float
    :type bet_id: unicode
    :type bsp_liability: float
    :type order_type: unicode
    :type persistence_type: unicode
    :type placed_date: datetime.datetime
    :type price: float
    :type side: unicode
    :type size: float
    :type size_cancelled: float
    :type size_lapsed: float
    :type size_matched: float
    :type size_remaining: float
    :type size_voided: float
    :type status: unicode
    """

    def __init__(
        self,
        betId: str,
        avgPriceMatched: float,
        bspLiability: float,
        orderType: str,
        persistenceType: str,
        price: float,
        side: str,
        sizeCancelled: float,
        sizeLapsed: float,
        sizeMatched: float,
        sizeRemaining: float,
        sizeVoided: float,
        status: str,
        size: float,
        customerStrategyRef: str = None,
        customerOrderRef: str = None,
        placedDate: str = None,
    ):
        self.bet_id = betId
        self.avg_price_matched = avgPriceMatched
        self.bsp_liability = bspLiability
        self.order_type = orderType
        self.persistence_type = persistenceType
        self.placed_date = BaseResource.strip_datetime(placedDate)
        self.price = price
        self.side = side
        self.size_cancelled = sizeCancelled
        self.size_lapsed = sizeLapsed
        self.size_matched = sizeMatched
        self.size_remaining = sizeRemaining
        self.size_voided = sizeVoided
        self.status = status
        self.size = size
        self.customer_strategy_ref = customerStrategyRef
        self.customer_order_ref = customerOrderRef


class RunnerBookMatch:
    """
    :type bet_id: unicode
    :type match_date: datetime.datetime
    :type match_id: unicode
    :type price: float
    :type side: unicode
    :type size: float
    """

    def __init__(
        self,
        price: float,
        side: str,
        size: float,
        betId: str = None,
        matchId: str = None,
        matchDate: str = None,
    ):
        self.bet_id = betId
        self.match_id = matchId
        self.price = price
        self.side = side
        self.size = size
        self.match_date = BaseResource.strip_datetime(matchDate)


class RunnerBook:
    """
    :type adjustment_factor: float
    :type ex: RunnerBookEX
    :type handicap: float
    :type last_price_traded: float
    :type matches: list[RunnerBookMatch]
    :type orders: list[RunnerBookOrder]
    :type removal_date: datetime.datetime
    :type selection_id: int
    :type sp: RunnerBookSP
    :type status: unicode
    :type total_matched: float
    """

    def __init__(
        self,
        selectionId: int,
        status: str,
        handicap: float,
        adjustmentFactor: float = None,
        lastPriceTraded: float = None,
        totalMatched: float = None,
        removalDate: str = None,
        sp: dict = None,
        ex: dict = None,
        orders: list = None,
        matches: list = None,
        matchesByStrategy: list = None,
    ):
        self.selection_id = selectionId
        self.status = status
        self.total_matched = totalMatched
        self.adjustment_factor = adjustmentFactor
        self.handicap = handicap
        self.last_price_traded = lastPriceTraded
        self.removal_date = BaseResource.strip_datetime(removalDate)
        self.sp = RunnerBookSP(**sp) if sp else None
        self.ex = RunnerBookEX(**ex) if ex else None
        self.orders = [RunnerBookOrder(**i) for i in orders] if orders else []
        self.matches = [RunnerBookMatch(**i) for i in matches] if matches else []
        self.matches_by_strategy = matchesByStrategy

    def __str__(self):
        return "RunnerBook: %s" % self.selection_id

    def __repr__(self):
        return "<RunnerBook>"


class KeyLine:
    def __init__(self, **kwargs):
        if "keyLine" in kwargs:
            self.key_line = [KeyLineSelection(**i) for i in kwargs["keyLine"]]
        elif "kl" in kwargs:
            self.key_line = [KeyLineSelection(**i) for i in kwargs["kl"]]


class KeyLineSelection:
    """
    :type selectionId: int
    :type handicap: float
    """

    def __init__(self, **kwargs):
        if "selectionId" in kwargs:
            self.selection_id = kwargs["selectionId"]
        elif "id" in kwargs:
            self.selection_id = kwargs["id"]

        if "handicap" in kwargs:
            self.handicap = kwargs["handicap"]
        elif "hc" in kwargs:
            self.handicap = kwargs["hc"]


class MarketBook(BaseResource):
    """
    :type bet_delay: int
    :type bsp_reconciled: bool
    :type complete: bool
    :type cross_matching: bool
    :type inplay: bool
    :type is_market_data_delayed: bool
    :type last_match_time: datetime.datetime
    :type market_id: unicode
    :type number_of_active_runners: int
    :type number_of_runners: int
    :type number_of_winners: int
    :type publish_time: datetime.datetime
    :type runners: list[RunnerBook]
    :type runners_voidable: bool
    :type status: unicode
    :type total_available: float
    :type total_matched: float
    :type version: int
    """

    def __init__(self, **kwargs):
        self.streaming_unique_id = kwargs.pop("streaming_unique_id", None)
        self.streaming_update = kwargs.pop("streaming_update", None)
        self.streaming_snap = kwargs.pop("streaming_snap", False)
        self.market_definition = kwargs.pop("market_definition", None)
        super(MarketBook, self).__init__(**kwargs)
        self.market_id = kwargs.get("marketId")
        self.bet_delay = kwargs.get("betDelay")
        self.bsp_reconciled = kwargs.get("bspReconciled")
        self.complete = kwargs.get("complete")
        self.cross_matching = kwargs.get("crossMatching")
        self.inplay = kwargs.get("inplay")
        self.is_market_data_delayed = kwargs.get("isMarketDataDelayed")
        self.last_match_time = self.strip_datetime(kwargs.get("lastMatchTime"))
        self.number_of_active_runners = kwargs.get("numberOfActiveRunners")
        self.number_of_runners = kwargs.get("numberOfRunners")
        self.number_of_winners = kwargs.get("numberOfWinners")
        self.runners_voidable = kwargs.get("runnersVoidable")
        self.status = kwargs.get("status")
        self.total_available = kwargs.get("totalAvailable")
        self.total_matched = kwargs.get("totalMatched")
        self.version = kwargs.get("version")
        self.runners = [RunnerBook(**i) for i in kwargs.get("runners")]
        self.publish_time = self.strip_datetime(kwargs.get("publishTime"))
        self.publish_time_epoch = kwargs.get("publishTime")
        self.key_line_description = (
            KeyLine(**kwargs.get("keyLineDescription"))
            if kwargs.get("keyLineDescription")
            else None
        )
        self.price_ladder_definition = (
            PriceLadderDescription(**kwargs.get("priceLadderDefinition"))
            if kwargs.get("priceLadderDefinition")
            else None
        )


class CurrentOrder:
    """
    :type average_price_matched: float
    :type bet_id: unicode
    :type bsp_liability: float
    :type customer_order_ref: unicode
    :type customer_strategy_ref: unicode
    :type handicap: float
    :type market_id: unicode
    :type matched_date: datetime.datetime
    :type order_type: unicode
    :type persistence_type: unicode
    :type placed_date: datetime.datetime
    :type price_size: PriceSize
    :type regulator_auth_code: unicode
    :type regulator_code: unicode
    :type selection_id: int
    :type side: unicode
    :type size_cancelled: float
    :type size_lapsed: float
    :type size_matched: float
    :type size_remaining: float
    :type size_voided: float
    :type status: unicode
    """

    def __init__(
        self,
        betId: str,
        averagePriceMatched: float,
        bspLiability: float,
        handicap: float,
        marketId: str,
        orderType: str,
        persistenceType: str,
        placedDate: str,
        regulatorCode: str,
        selectionId: int,
        side: str,
        sizeCancelled: float,
        sizeLapsed: float,
        sizeMatched: float,
        sizeRemaining: float,
        sizeVoided: float,
        status: str,
        priceSize: dict,
        matchedDate: str = None,
        customerStrategyRef: str = None,
        customerOrderRef: str = None,
        regulatorAuthCode: str = None,
        lapsedDate: str = None,
        lapseStatusReasonCode: str = None,
        cancelledDate: str = None,
    ):
        self.bet_id = betId
        self.average_price_matched = averagePriceMatched
        self.bsp_liability = bspLiability
        self.handicap = handicap
        self.market_id = marketId
        self.matched_date = BaseResource.strip_datetime(matchedDate)
        self.order_type = orderType
        self.persistence_type = persistenceType
        self.placed_date = BaseResource.strip_datetime(placedDate)
        self.regulator_auth_code = regulatorAuthCode
        self.regulator_code = regulatorCode
        self.selection_id = selectionId
        self.side = side
        self.size_cancelled = sizeCancelled
        self.size_lapsed = sizeLapsed
        self.size_matched = sizeMatched
        self.size_remaining = sizeRemaining
        self.size_voided = sizeVoided
        self.status = status
        self.customer_strategy_ref = customerStrategyRef
        self.customer_order_ref = customerOrderRef
        self.price_size = PriceSize(**priceSize)
        self.lapsed_date = BaseResource.strip_datetime(lapsedDate)
        self.lapse_status_reason_code = lapseStatusReasonCode
        self.cancelled_date = BaseResource.strip_datetime(cancelledDate)


class Match:
    def __init__(self, selectionId: int, matchedLays: list, matchedBacks: list):
        self.selection_id = selectionId
        self.matched_lays = [PriceSize(**m) for m in matchedLays]
        self.matched_backs = [PriceSize(**m) for m in matchedBacks]


class CurrentOrders(BaseResource):
    """
    :type more_available: bool
    :type orders: list[CurrentOrder]
    """

    def __init__(self, **kwargs):
        self.streaming_unique_id = kwargs.pop("streaming_unique_id", None)
        self.streaming_update = kwargs.pop("streaming_update", None)
        self.streaming_snap = kwargs.pop("streaming_snap", False)
        self.publish_time = kwargs.pop("publish_time", None)
        super(CurrentOrders, self).__init__(**kwargs)
        self.more_available = kwargs.get("moreAvailable")
        self.orders = [CurrentOrder(**i) for i in kwargs.get("currentOrders")]
        self.matches = [Match(**i) for i in kwargs.get("matches", [])]


class ItemDescription:
    """
    :type event_desc: unicode
    :type event_type_desc: unicode
    :type market_desc: unicode
    :type market_start_time: datetime
    :type market_type: unicode
    :type number_of_winners: int
    :type runner_desc: unicode
    :type each_way_divisor: unicode
    """

    def __init__(
        self,
        eventDesc: str = None,
        eventTypeDesc: str = None,
        marketDesc: str = None,
        marketStartTime: str = None,
        marketType: str = None,
        numberOfWinners: int = None,
        runnerDesc: str = None,
        eachWayDivisor: float = None,
    ):
        self.event_desc = eventDesc
        self.event_type_desc = eventTypeDesc
        self.market_desc = marketDesc
        self.market_start_time = BaseResource.strip_datetime(marketStartTime)
        self.market_type = marketType
        self.number_of_winners = numberOfWinners
        self.runner_desc = runnerDesc
        self.each_way_divisor = eachWayDivisor


class ClearedOrder:
    """
    :type bet_count: int
    :type bet_id: unicode
    :type bet_outcome: unicode
    :type customer_order_ref: unicode
    :type customer_strategy_ref: unicode
    :type event_id: unicode
    :type event_type_id: unicode
    :type handicap: float
    :type last_matched_date: datetime.datetime
    :type market_id: unicode
    :type order_type: unicode
    :type persistence_type: unicode
    :type placed_date: datetime.datetime
    :type price_matched: float
    :type price_reduced: bool
    :type price_requested: float
    :type profit: float
    :type commission: float
    :type selection_id: int
    :type settled_date: datetime.datetime
    :type side: unicode
    :type size_settled: float
    :type size_cancelled float
    :type item_description ItemDescription
    """

    def __init__(self, **kwargs):
        self.bet_id = kwargs.get("betId")
        self.bet_count = kwargs.get("betCount")
        self.bet_outcome = kwargs.get("betOutcome")
        self.event_id = kwargs.get("eventId")
        self.event_type_id = kwargs.get("eventTypeId")
        self.handicap = kwargs.get("handicap")
        self.last_matched_date = BaseResource.strip_datetime(
            kwargs.get("lastMatchedDate")
        )
        self.market_id = kwargs.get("marketId")
        self.order_type = kwargs.get("orderType")
        self.persistence_type = kwargs.get("persistenceType")
        self.placed_date = BaseResource.strip_datetime(kwargs.get("placedDate"))
        self.price_matched = kwargs.get("priceMatched")
        self.price_reduced = kwargs.get("priceReduced")
        self.price_requested = kwargs.get("priceRequested")
        self.profit = kwargs.get("profit")
        self.commission = kwargs.get("commission")
        self.selection_id = kwargs.get("selectionId")
        self.settled_date = BaseResource.strip_datetime(kwargs.get("settledDate"))
        self.side = kwargs.get("side")
        self.size_settled = kwargs.get("sizeSettled")
        self.size_cancelled = kwargs.get("sizeCancelled")
        self.customer_strategy_ref = kwargs.get("customerStrategyRef")
        self.customer_order_ref = kwargs.get("customerOrderRef")
        self.item_description = (
            ItemDescription(**kwargs.get("itemDescription"))
            if "itemDescription" in kwargs
            else None
        )


class ClearedOrders(BaseResource):
    """
    :type more_available: bool
    :type orders: list[ClearedOrder]
    """

    def __init__(self, **kwargs):
        super(ClearedOrders, self).__init__(**kwargs)
        self.more_available = kwargs.get("moreAvailable")
        self.orders = [ClearedOrder(**i) for i in kwargs.get("clearedOrders")]


class ProfitAndLosses:
    """
    :type if_lose: float
    :type if_place: float
    :type if_win: float
    :type selection_id: int
    """

    def __init__(
        self,
        selectionId: int,
        ifWin: float = None,
        ifLose: float = None,
        ifPlace: float = None,
    ):
        self.selection_id = selectionId
        self.if_win = ifWin
        self.if_lose = ifLose
        self.if_place = ifPlace


class MarketProfitLoss(BaseResource):
    """
    :type commission_applied: float
    :type market_id: unicode
    :type profit_and_losses: list[ProfitAndLosses]
    """

    def __init__(self, **kwargs):
        super(MarketProfitLoss, self).__init__(**kwargs)
        self.market_id = kwargs.get("marketId")
        self.commission_applied = kwargs.get("commissionApplied")
        self.profit_and_losses = [
            ProfitAndLosses(**i) for i in kwargs.get("profitAndLosses")
        ]


class LimitOrder:
    """
    :type bet_target_size: float
    :type bet_target_type: unicode
    :type min_fill_size: float
    :type persistence_type: unicode
    :type price: float
    :type size: float
    :type time_in_force: unicode
    """

    def __init__(
        self,
        price: float,
        size: float = None,
        persistenceType: str = None,
        timeInForce: str = None,
        minFillSize: float = None,
        betTargetType: str = None,
        betTargetSize: float = None,
    ):
        self.persistence_type = persistenceType
        self.price = price
        self.size = size
        self.time_in_force = timeInForce
        self.min_fill_size = minFillSize
        self.bet_target_type = betTargetType
        self.bet_target_size = betTargetSize


class LimitOnCloseOrder:
    """
    :type liability: float
    :type price: float
    """

    def __init__(self, liability: float, price: float):
        self.liability = liability
        self.price = price


class MarketOnCloseOrder:
    """
    :type liability: float
    """

    def __init__(self, liability: float):
        self.liability = liability


class PlaceOrderInstruction:
    """
    :type customer_order_ref: unicode
    :type handicap: float
    :type order: LimitOrder
    :type order_type: unicode
    :type selection_id: int
    :type side: unicode
    """

    def __init__(
        self,
        selectionId: int,
        side: str,
        orderType: str,
        limitOrder: dict = None,
        limitOnCloseOrder: dict = None,
        marketOnCloseOrder: dict = None,
        handicap: float = None,
        customerOrderRef: str = None,
    ):
        self.selection_id = selectionId
        self.side = side
        self.order_type = orderType
        self.handicap = handicap
        self.customer_order_ref = customerOrderRef
        self.limit_order = LimitOrder(**limitOrder) if limitOrder else None
        self.limit_on_close_order = (
            LimitOnCloseOrder(**limitOnCloseOrder) if limitOnCloseOrder else None
        )
        self.market_on_close_order = (
            MarketOnCloseOrder(**marketOnCloseOrder) if marketOnCloseOrder else None
        )


class PlaceOrderInstructionReports:
    """
    :type average_price_matched: float
    :type bet_id: unicode
    :type error_code: str
    :type instruction: PlaceOrderInstruction
    :type order_status: unicode
    :type placed_date: datetime.datetime
    :type size_matched: float
    :type status: unicode
    """

    def __init__(
        self,
        status: str,
        instruction: dict = None,
        orderStatus: str = None,
        betId: int = None,
        averagePriceMatched: float = None,
        sizeMatched: float = None,
        placedDate: str = None,
        errorCode: str = None,
    ):
        self.status = status
        self.order_status = orderStatus
        self.bet_id = betId
        self.average_price_matched = averagePriceMatched
        self.size_matched = sizeMatched
        self.placed_date = BaseResource.strip_datetime(placedDate)
        self.instruction = PlaceOrderInstruction(**instruction) if instruction else None
        self.error_code = errorCode


class PlaceOrders(BaseResource):
    """
    :type customer_ref: unicode
    :type error_code: str
    :type market_id: unicode
    :type place_instruction_reports: list[PlaceOrderInstructionReports]
    :type status: unicode
    """

    def __init__(self, **kwargs):
        super(PlaceOrders, self).__init__(**kwargs)
        self.market_id = kwargs.get("marketId")
        self.status = kwargs.get("status")
        self.customer_ref = kwargs.get("customerRef")
        self.error_code = kwargs.get("errorCode")
        self.place_instruction_reports = [
            PlaceOrderInstructionReports(**i) for i in kwargs.get("instructionReports")
        ]


class CancelOrderInstruction:
    """
    :type bet_id: unicode
    :type size_reduction: float
    """

    def __init__(self, betId: str, sizeReduction: float = None):
        self.bet_id = betId
        self.size_reduction = sizeReduction


class CancelOrderInstructionReports:
    """
    :type cancelled_date: datetime.datetime
    :type error_code: str
    :type instruction: CancelOrderInstruction
    :type size_cancelled: float
    :type status: unicode
    """

    def __init__(
        self,
        status: str,
        instruction: dict,
        sizeCancelled: float = None,
        cancelledDate: str = None,
        errorCode: str = None,
    ):
        self.status = status
        self.size_cancelled = sizeCancelled
        self.cancelled_date = BaseResource.strip_datetime(cancelledDate)
        self.instruction = CancelOrderInstruction(**instruction)
        self.error_code = errorCode


class CancelOrders(BaseResource):
    """
    :type cancel_instruction_reports: list[CancelOrderInstructionReports]
    :type customer_ref: unicode
    :type error_code: str
    :type market_id: unicode
    :type status: unicode
    """

    def __init__(self, **kwargs):
        super(CancelOrders, self).__init__(**kwargs)
        self.market_id = kwargs.get("marketId")
        self.status = kwargs.get("status")
        self.customer_ref = kwargs.get("customerRef")
        self.error_code = kwargs.get("errorCode")
        self.cancel_instruction_reports = [
            CancelOrderInstructionReports(**i) for i in kwargs.get("instructionReports")
        ]


class UpdateOrderInstruction:
    """
    :type bet_id: unicode
    :type new_persistence_type: unicode
    """

    def __init__(self, betId: str, newPersistenceType: str):
        self.bet_id = betId
        self.new_persistence_type = newPersistenceType


class UpdateOrderInstructionReports:
    """
    :type error_code: str
    :type instruction: UpdateOrderInstruction
    :type status: unicode
    """

    def __init__(self, status: str, instruction: dict, errorCode: str = None):
        self.status = status
        self.instruction = UpdateOrderInstruction(**instruction)
        self.error_code = errorCode


class UpdateOrders(BaseResource):
    """
    :type customer_ref: unicode
    :type error_code: str
    :type market_id: unicode
    :type status: unicode
    :type update_instruction_reports: list[UpdateOrderInstructionReports]
    """

    def __init__(self, **kwargs):
        super(UpdateOrders, self).__init__(**kwargs)
        self.market_id = kwargs.get("marketId")
        self.status = kwargs.get("status")
        self.customer_ref = kwargs.get("customerRef")
        self.error_code = kwargs.get("errorCode")
        self.update_instruction_reports = [
            UpdateOrderInstructionReports(**i) for i in kwargs.get("instructionReports")
        ]


class ReplaceOrderInstructionReports:
    """
    :type cancel_instruction_reports: CancelOrderInstructionReports
    :type error_code: str
    :type place_instruction_reports: PlaceOrderInstructionReports
    :type status: unicode
    """

    def __init__(
        self,
        status: str,
        cancelInstructionReport: dict,
        placeInstructionReport: dict,
        errorCode: str = None,
    ):
        self.status = status
        self.cancel_instruction_reports = CancelOrderInstructionReports(
            **cancelInstructionReport
        )
        self.place_instruction_reports = PlaceOrderInstructionReports(
            **placeInstructionReport
        )
        self.error_code = errorCode


class ReplaceOrders(BaseResource):
    """
    :type customer_ref: unicode
    :type error_code: str
    :type market_id: unicode
    :type replace_instruction_reports: list[ReplaceOrderInstructionReports]
    :type status: unicode
    """

    def __init__(self, **kwargs):
        super(ReplaceOrders, self).__init__(**kwargs)
        self.market_id = kwargs.get("marketId")
        self.status = kwargs.get("status")
        self.customer_ref = kwargs.get("customerRef")
        self.error_code = kwargs.get("errorCode")
        self.replace_instruction_reports = [
            ReplaceOrderInstructionReports(**i)
            for i in kwargs.get("instructionReports")
        ]
