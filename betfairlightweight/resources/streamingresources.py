from .baseresource import BaseResource
from .bettingresources import PriceLadderDescription


class MarketDefinitionRunner:
    """
    :type adjustment_factor: float
    :type id: int
    :type removal_date: datetime.datetime
    :type sort_priority: int
    :type status: unicode
    """

    def __init__(
        self,
        id: int,
        sortPriority: int,
        status: str,
        hc: float = 0,
        bsp: float = None,
        adjustmentFactor: float = None,
        removalDate: str = None,
        name: str = None,
    ):
        self.selection_id = id
        self.sort_priority = sortPriority
        self.status = status
        self.handicap = hc
        self.bsp = bsp
        self.adjustment_factor = adjustmentFactor
        self.removal_date = BaseResource.strip_datetime(removalDate)
        self.name = name  # historic data only

    def __str__(self):
        return "MarketDefinitionRunner: %s" % self.selection_id

    def __repr__(self):
        return "<MarketDefinitionRunner>"


class MarketDefinitionKeyLineSelection:
    """
    :type selectionId: int
    :type handicap: float
    """

    def __init__(self, **kwargs):
        self.selection_id = kwargs.get("id")
        self.handicap = kwargs.get("hc")


class MarketDefinitionKeyLine:
    def __init__(self, kl):
        self.key_line = [MarketDefinitionKeyLineSelection(**i) for i in kl]


class MarketDefinition:
    """
    :type bet_delay: int
    :type betting_type: unicode
    :type bsp_market: bool
    :type bsp_reconciled: bool
    :type complete: bool
    :type country_code: unicode
    :type cross_matching: bool
    :type discount_allowed: bool
    :type event_id: unicode
    :type event_type_id: unicode
    :type in_play: bool
    :type market_base_rate: float
    :type market_time: datetime.datetime
    :type market_type: unicode
    :type number_of_active_runners: int
    :type number_of_winners: int
    :type open_date: datetime.datetime
    :type persistence_enabled: bool
    :type regulators: unicode
    :type runners: list[MarketDefinitionRunner]
    :type runners_voidable: bool
    :type settled_time: datetime.datetime
    :type status: unicode
    :type suspend_time: datetime.datetime
    :type timezone: unicode
    :type turn_in_play_enabled: bool
    :type venue: unicode
    :type version: int
    """

    def __init__(
        self,
        betDelay: int,
        bettingType: str,
        bspMarket: bool,
        bspReconciled: bool,
        complete: bool,
        crossMatching: bool,
        discountAllowed: bool,
        eventId: str,
        eventTypeId: str,
        inPlay: bool,
        marketBaseRate: float,
        marketTime: str,
        numberOfActiveRunners: int,
        numberOfWinners: int,
        persistenceEnabled: bool,
        regulators: str,
        runnersVoidable: bool,
        status: str,
        timezone: str,
        turnInPlayEnabled: bool,
        version: int,
        runners: list,
        openDate: str = None,
        countryCode: str = None,
        eachWayDivisor: float = None,
        venue: str = None,
        settledTime: str = None,
        suspendTime: str = None,
        marketType: str = None,
        lineMaxUnit: float = None,
        lineMinUnit: float = None,
        lineInterval: float = None,
        name: str = None,
        eventName: str = None,
        priceLadderDefinition: dict = None,
        keyLineDefinition: dict = None,
        raceType: str = None,
    ):
        self.bet_delay = betDelay
        self.betting_type = bettingType
        self.bsp_market = bspMarket
        self.bsp_reconciled = bspReconciled
        self.complete = complete
        self.country_code = countryCode
        self.cross_matching = crossMatching
        self.discount_allowed = discountAllowed
        self.event_id = eventId
        self.event_type_id = eventTypeId
        self.in_play = inPlay
        self.market_base_rate = marketBaseRate
        self.market_time = BaseResource.strip_datetime(marketTime)
        self.market_type = marketType
        self.number_of_active_runners = numberOfActiveRunners
        self.number_of_winners = numberOfWinners
        self.open_date = BaseResource.strip_datetime(openDate) if openDate else None
        self.persistence_enabled = persistenceEnabled
        self.regulators = regulators
        self.runners_voidable = runnersVoidable
        self.settled_time = BaseResource.strip_datetime(settledTime)
        self.status = status
        self.each_way_divisor = eachWayDivisor
        self.suspend_time = BaseResource.strip_datetime(suspendTime)
        self.timezone = timezone
        self.turn_in_play_enabled = turnInPlayEnabled
        self.venue = venue
        self.version = version
        self.line_max_unit = lineMaxUnit
        self.line_min_unit = lineMinUnit
        self.line_interval = lineInterval
        self.runners = [MarketDefinitionRunner(**i) for i in runners]
        self.price_ladder_definition = (
            PriceLadderDescription(**priceLadderDefinition)
            if priceLadderDefinition
            else None
        )
        self.key_line_definitions = (
            MarketDefinitionKeyLine(**keyLineDefinition) if keyLineDefinition else None
        )
        self.race_type = raceType

        self.name = name  # historic data only
        self.event_name = eventName  # historic data only
