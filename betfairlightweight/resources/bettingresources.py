from .baseresource import BaseResource


class EventType(BaseResource):
    """
    :type id: unicode
    :type name: unicode
    """
    id = None
    name = None

    class Meta(BaseResource.Meta):
        identifier = 'event_type'
        attributes = {
            'id': 'id',
            'name': 'name'
        }


class EventTypeResult(BaseResource):
    """
    :type event_type: EventType
    :type market_count: int
    """
    event_type = None
    market_count = None

    class Meta(BaseResource.Meta):
        identifier = 'event_type_result'
        attributes = {
            'marketCount': 'market_count'
        }
        sub_resources = {
            'eventType': EventType
        }


class Competition(BaseResource):
    """
    :type id: unicode
    :type name: unicode
    """
    id = None
    name = None

    class Meta(BaseResource.Meta):
        identifier = 'competition'
        attributes = {
            'id': 'id',
            'name': 'name'
        }


class CompetitionResult(BaseResource):
    """
    :type competition: Competition
    :type competition_region: unicode
    :type market_count: int
    """
    competition = None
    competition_region = None
    market_count = None

    class Meta(BaseResource.Meta):
        identifier = 'competition_result'
        attributes = {
            'marketCount': 'market_count',
            'competitionRegion': 'competition_region'
        }
        sub_resources = {
            'competition': Competition
        }


class TimeRange(BaseResource):
    """
    :type _from: datetime.datetime
    :type to: datetime.datetime
    """
    _from = None
    to = None

    class Meta(BaseResource.Meta):
        identifier = 'time_range'
        attributes = {
            'from': '_from',
            'to': 'to'
        }
        datetime_attributes = (
            'from',
            'to'
        )


class TimeRangeResult(BaseResource):
    """
    :type market_count: int
    :type time_range: TimeRange
    """
    market_count = None
    time_range = None

    class Meta(BaseResource.Meta):
        identifier = 'time_range_result'
        attributes = {
            'marketCount': 'market_count'
        }
        sub_resources = {
            'timeRange': TimeRange
        }


class Event(BaseResource):
    """
    :type country_code: unicode
    :type id: unicode
    :type name: unicode
    :type open_date: datetime.datetime
    :type time_zone: unicode
    :type venue: unicode
    """
    country_code = None
    id = None
    name = None
    open_date = None
    time_zone = None
    venue = None

    class Meta(BaseResource.Meta):
        identifier = 'event'
        attributes = {
            'id': 'id',
            'openDate': 'open_date',
            'timezone': 'time_zone',
            'countryCode': 'country_code',
            'name': 'name',
            'venue': 'venue'
        }
        datetime_attributes = (
            'openDate'
        )


class EventResult(BaseResource):
    """
    :type event: Event
    :type market_count: int
    """
    event = None
    market_count = None

    class Meta(BaseResource.Meta):
        identifier = 'event_result'
        attributes = {
            'marketCount': 'market_count'
        }
        sub_resources = {
            'event': Event
        }


class MarketTypeResult(BaseResource):
    """
    :type market_count: int
    :type market_type: unicode
    """
    market_count = None
    market_type = None

    class Meta(BaseResource.Meta):
        identifier = 'market_type_result'
        attributes = {
            'marketCount': 'market_count',
            'marketType': 'market_type'
        }


class CountryResult(BaseResource):
    """
    :type country_code: unicode
    :type market_count: int
    """
    country_code = None
    market_count = None

    class Meta(BaseResource.Meta):
        identifier = 'country_result'
        attributes = {
            'marketCount': 'market_count',
            'countryCode': 'country_code'
        }


class VenueResult(BaseResource):
    """
    :type market_count: int
    :type venue: unicode
    """
    market_count = None
    venue = None

    class Meta(BaseResource.Meta):
        identifier = 'venue_result'
        attributes = {
            'marketCount': 'market_count',
            'venue': 'venue'
        }


class MarketCatalogueDescription(BaseResource):
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
    betting_type = None
    bsp_market = None
    clarifications = None
    discount_allowed = None
    each_way_divisor = None
    market_base_rate = None
    market_time = None
    market_type = None
    persistence_enabled = None
    regulator = None
    rules = None
    rules_has_date = None
    suspend_time = None
    turn_in_play_enabled = None
    wallet = None

    class Meta(BaseResource.Meta):
        identifier = 'description'
        attributes = {
            'bettingType': 'betting_type',
            'bspMarket': 'bsp_market',
            'discountAllowed': 'discount_allowed',
            'marketBaseRate': 'market_base_rate',
            'marketTime': 'market_time',
            'marketType': 'market_type',
            'persistenceEnabled': 'persistence_enabled',
            'regulator': 'regulator',
            'rules': 'rules',
            'rulesHasDate': 'rules_has_date',
            'suspendTime': 'suspend_time',
            'turnInPlayEnabled': 'turn_in_play_enabled',
            'wallet': 'wallet',
            'eachWayDivisor': 'each_way_divisor',
            'clarifications': 'clarifications'
        }
        datetime_attributes = (
            'marketTime',
            'suspendTime'
        )


class RunnerCatalogue(BaseResource):
    """
    :type handicap: float
    :type metadata: dict
    :type runner_name: unicode
    :type selection_id: int
    :type sort_priority: int
    """
    handicap = None
    metadata = None
    runner_name = None
    selection_id = None
    sort_priority = None

    class Meta(BaseResource.Meta):
        identifier = 'runners'
        attributes = {
            'selectionId': 'selection_id',
            'runnerName': 'runner_name',
            'sortPriority': 'sort_priority',
            'handicap': 'handicap',
            'metadata': 'metadata'
        }


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
    competition = None
    description = None
    event = None
    event_type = None
    market_id = None
    market_name = None
    market_start_time = None
    runners = None
    total_matched = None

    class Meta(BaseResource.Meta):
        identifier = 'market_catalogue'
        attributes = {
            'marketId': 'market_id',
            'marketName': 'market_name',
            'totalMatched': 'total_matched',
            'marketStartTime': 'market_start_time'
        }
        sub_resources = {
            'competition': Competition,
            'event': Event,
            'eventType': EventType,
            'description': MarketCatalogueDescription,
            'runners': RunnerCatalogue
        }
        datetime_attributes = (
            'marketStartTime'
        )


class PriceSize(BaseResource):
    """
    :type price: float
    :type size: float
    """
    price = None
    size = None

    class Meta(BaseResource.Meta):
        identifier = 'price_size'
        attributes = {
            'price': 'price',
            'size': 'size'
        }


class RunnerBookSP(BaseResource):
    """
    :type actual_sp: float
    :type back_stake_taken: list[PriceSize]
    :type far_price: float
    :type lay_liability_taken: list[PriceSize]
    :type near_price: float
    """
    actual_sp = None
    back_stake_taken = None
    far_price = None
    lay_liability_taken = None
    near_price = None

    class Meta(BaseResource.Meta):
        identifier = 'sp'
        attributes = {
            'nearPrice': 'near_price',
            'farPrice': 'far_price',
            'backStakeTaken': 'back_stake_taken',
            'layLiabilityTaken': 'lay_liability_taken',
            'actualSP': 'actual_sp'
        }
        sub_resources = {
            'backStakeTaken': PriceSize,
            'layLiabilityTaken': PriceSize
        }


class RunnerBookEX(BaseResource):
    """
    :type available_to_back: list[PriceSize]
    :type available_to_lay: list[PriceSize]
    :type traded_volume: list[PriceSize]
    """
    available_to_back = None
    available_to_lay = None
    traded_volume = None

    class Meta(BaseResource.Meta):
        identifier = 'ex'
        attributes = {
            'availableToBack': 'available_to_back',
            'availableToLay': 'available_to_lay',
            'tradedVolume': 'traded_volume'
        }
        sub_resources = {
            'availableToBack': PriceSize,
            'availableToLay': PriceSize,
            'tradedVolume': PriceSize
        }


class RunnerBookOrder(BaseResource):
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
    avg_price_matched = None
    bet_id = None
    bsp_liability = None
    order_type = None
    persistence_type = None
    placed_date = None
    price = None
    side = None
    size = None
    size_cancelled = None
    size_lapsed = None
    size_matched = None
    size_remaining = None
    size_voided = None
    status = None

    class Meta(BaseResource.Meta):
        identifier = 'orders'
        attributes = {
            'betId': 'bet_id',
            'avgPriceMatched': 'avg_price_matched',
            'bspLiability': 'bsp_liability',
            'orderType': 'order_type',
            'persistenceType': 'persistence_type',
            'placedDate': 'placed_date',
            'price': 'price',
            'side': 'side',
            'size': 'size',
            'sizeCancelled': 'size_cancelled',
            'sizeLapsed': 'size_lapsed',
            'sizeMatched': 'size_matched',
            'sizeRemaining': 'size_remaining',
            'sizeVoided': 'size_voided',
            'status': 'status'
        }
        datetime_attributes = (
            'placedDate'
        )


class RunnerBookMatch(BaseResource):
    """
    :type bet_id: unicode
    :type match_date: datetime.datetime
    :type match_id: unicode
    :type price: float
    :type side: unicode
    :type size: float
    """
    bet_id = None
    match_date = None
    match_id = None
    price = None
    side = None
    size = None

    class Meta(BaseResource.Meta):
        identifier = 'matches'
        attributes = {
            'betId': 'bet_id',
            'matchId': 'match_id',
            'price': 'price',
            'side': 'side',
            'size': 'size',
            'matchDate': 'match_date'
        }
        datetime_attributes = (
            'matchDate'
        )


class RunnerBook(BaseResource):
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
    adjustment_factor = None
    ex = None
    handicap = None
    last_price_traded = None
    matches = None
    orders = None
    removal_date = None
    selection_id = None
    sp = None
    status = None
    total_matched = None

    class Meta(BaseResource.Meta):
        identifier = 'runners'
        attributes = {
            'selectionId': 'selection_id',
            'status': 'status',
            'totalMatched': 'total_matched',
            'adjustmentFactor': 'adjustment_factor',
            'handicap': 'handicap',
            'lastPriceTraded': 'last_price_traded',
            'removalDate': 'removal_date',
        }
        sub_resources = {
            'sp': RunnerBookSP,
            'ex': RunnerBookEX,
            'orders': RunnerBookOrder,
            'matches': RunnerBookMatch
        }
        datetime_attributes = (
            'removalDate',
        )


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
    bet_delay = None
    bsp_reconciled = None
    complete = None
    cross_matching = None
    inplay = None
    is_market_data_delayed = None
    last_match_time = None
    market_id = None
    number_of_active_runners = None
    number_of_runners = None
    number_of_winners = None
    publish_time = None
    runners = None
    runners_voidable = None
    status = None
    total_available = None
    total_matched = None
    version = None

    class Meta(BaseResource.Meta):
        identifier = 'market_book'
        attributes = {
            'marketId': 'market_id',
            'betDelay': 'bet_delay',
            'bspReconciled': 'bsp_reconciled',
            'complete': 'complete',
            'crossMatching': 'cross_matching',
            'inplay': 'inplay',
            'isMarketDataDelayed': 'is_market_data_delayed',
            'lastMatchTime': 'last_match_time',
            'numberOfActiveRunners': 'number_of_active_runners',
            'numberOfRunners': 'number_of_runners',
            'numberOfWinners': 'number_of_winners',
            'runnersVoidable': 'runners_voidable',
            'status': 'status',
            'totalAvailable': 'total_available',
            'totalMatched': 'total_matched',
            'version': 'version',
            'publishTime': 'publish_time',
        }
        sub_resources = {
            'runners': RunnerBook
        }
        datetime_attributes = (
            'lastMatchTime',
            'publishTime',
        )


class CurrentOrder(BaseResource):
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
    average_price_matched = None
    bet_id = None
    bsp_liability = None
    customer_order_ref = None
    customer_strategy_ref = None
    handicap = None
    market_id = None
    matched_date = None
    order_type = None
    persistence_type = None
    placed_date = None
    price_size = None
    regulator_code = None
    selection_id = None
    side = None
    size_cancelled = None
    size_lapsed = None
    size_matched = None
    size_remaining = None
    size_voided = None
    status = None

    class Meta(BaseResource.Meta):
        identifier = 'orders'
        attributes = {
            'betId': 'bet_id',
            'averagePriceMatched': 'average_price_matched',
            'bspLiability': 'bsp_liability',
            'handicap': 'handicap',
            'marketId': 'market_id',
            'matchedDate': 'matched_date',
            'orderType': 'order_type',
            'persistenceType': 'persistence_type',
            'placedDate': 'placed_date',
            'regulatorCode': 'regulator_code',
            'selectionId': 'selection_id',
            'side': 'side',
            'sizeCancelled': 'size_cancelled',
            'sizeLapsed': 'size_lapsed',
            'sizeMatched': 'size_matched',
            'sizeRemaining': 'size_remaining',
            'sizeVoided': 'size_voided',
            'status': 'status',
            'customerStrategyRef': 'customer_strategy_ref',
            'customerOrderRef': 'customer_order_ref'
        }
        sub_resources = {
            'priceSize': PriceSize
        }
        datetime_attributes = (
            'placedDate',
            'matchedDate'
        )


class CurrentOrders(BaseResource):
    """
    :type more_available: bool
    :type orders: list[CurrentOrder]
    """
    more_available = None
    orders = None

    class Meta(BaseResource.Meta):
        identifier = 'current_orders'
        attributes = {
            'moreAvailable': 'more_available'
        }
        sub_resources = {
            'currentOrders': CurrentOrder
        }


class ClearedOrder(BaseResource):
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
    :type selection_id: int
    :type settled_date: datetime.datetime
    :type side: unicode
    :type size_settled: float
    """
    bet_count = None
    bet_id = None
    bet_outcome = None
    customer_order_ref = None
    customer_strategy_ref = None
    event_id = None
    event_type_id = None
    handicap = None
    last_matched_date = None
    market_id = None
    order_type = None
    persistence_type = None
    placed_date = None
    price_matched = None
    price_reduced = None
    price_requested = None
    profit = None
    selection_id = None
    settled_date = None
    side = None
    size_settled = None

    class Meta(BaseResource.Meta):
        identifier = 'orders'
        attributes = {
            'betId': 'bet_id',
            'betCount': 'bet_count',
            'betOutcome': 'bet_outcome',
            'eventId': 'event_id',
            'eventTypeId': 'event_type_id',
            'handicap': 'handicap',
            'lastMatchedDate': 'last_matched_date',
            'marketId': 'market_id',
            'orderType': 'order_type',
            'persistenceType': 'persistence_type',
            'placedDate': 'placed_date',
            'priceMatched': 'price_matched',
            'priceReduced': 'price_reduced',
            'priceRequested': 'price_requested',
            'profit': 'profit',
            'selectionId': 'selection_id',
            'settledDate': 'settled_date',
            'side': 'side',
            'sizeSettled': 'size_settled',
            'customerStrategyRef': 'customer_strategy_ref',
            'customerOrderRef': 'customer_order_ref'
        }
        datetime_attributes = (
            'placedDate',
            'lastMatchedDate',
            'settledDate'
        )


class ClearedOrders(BaseResource):
    """
    :type more_available: bool
    :type orders: list[ClearedOrder]
    """
    more_available = None
    orders = None

    class Meta(BaseResource.Meta):
        identifier = 'cleared_orders'
        attributes = {
            'moreAvailable': 'more_available'
        }
        sub_resources = {
            'clearedOrders': ClearedOrder
        }


class ProfitAndLosses(BaseResource):
    """
    :type if_lose: float
    :type if_place: float
    :type if_win: float
    :type selection_id: int
    """
    if_lose = None
    if_place = None
    if_win = None
    selection_id = None

    class Meta(BaseResource.Meta):
        identifier = 'profit_and_losses'
        attributes = {
            'selectionId': 'selection_id',
            'ifWin': 'if_win',
            'ifLose': 'if_lose',
            'ifPlace': 'if_place'
        }


class MarketProfitLoss(BaseResource):
    """
    :type commission_applied: float
    :type market_id: unicode
    :type profit_and_losses: list[ProfitAndLosses]
    """
    commission_applied = None
    market_id = None
    profit_and_losses = None

    class Meta(BaseResource.Meta):
        identifier = 'market_profit_loss'
        attributes = {
            'marketId': 'market_id',
            'commissionApplied': 'commission_applied'
        }
        sub_resources = {
            'profitAndLosses': ProfitAndLosses
        }


class LimitOrder(BaseResource):
    """
    :type bet_target_size: float
    :type bet_target_type: unicode
    :type min_fill_size: float
    :type persistence_type: unicode
    :type price: float
    :type size: float
    :type time_in_force: unicode
    """
    bet_target_size = None
    bet_target_type = None
    min_fill_size = None
    persistence_type = None
    price = None
    size = None
    time_in_force = None

    class Meta(BaseResource.Meta):
        identifier = 'order'
        attributes = {
            'persistenceType': 'persistence_type',
            'price': 'price',
            'size': 'size',
            'timeInForce': 'time_in_force',
            'minFillSize': 'min_fill_size',
            'betTargetType': 'bet_target_type',
            'betTargetSize': 'bet_target_size'
        }


class PlaceOrderInstruction(BaseResource):
    """
    :type customer_order_ref: unicode
    :type handicap: float
    :type order: LimitOrder
    :type order_type: unicode
    :type selection_id: int
    :type side: unicode
    """
    customer_order_ref = None
    handicap = None
    order = None
    order_type = None
    selection_id = None
    side = None

    class Meta(BaseResource.Meta):
        identifier = 'instruction'
        attributes = {
            'selectionId': 'selection_id',
            'side': 'side',
            'orderType': 'order_type',
            'handicap': 'handicap',
            'customerOrderRef': 'customer_order_ref'
        }
        sub_resources = {
            'limitOrder': LimitOrder
        }


class PlaceOrderInstructionReports(BaseResource):
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
    average_price_matched = None
    bet_id = None
    error_code = None
    instruction = None
    order_status = None
    placed_date = None
    size_matched = None
    status = None

    class Meta(BaseResource.Meta):
        identifier = 'place_instruction_reports'
        attributes = {
            'status': 'status',
            'orderStatus': 'order_status',
            'betId': 'bet_id',
            'averagePriceMatched': 'average_price_matched',
            'sizeMatched': 'size_matched',
            'placedDate': 'placed_date',
            'errorCode': 'error_code',
        }
        sub_resources = {
            'instruction': PlaceOrderInstruction
        }
        datetime_attributes = (
            'placedDate'
        )


class PlaceOrders(BaseResource):
    """
    :type customer_ref: unicode
    :type error_code: str
    :type market_id: unicode
    :type place_instruction_reports: list[PlaceOrderInstructionReports]
    :type status: unicode
    """
    customer_ref = None
    error_code = None
    market_id = None
    place_instruction_reports = None
    status = None

    class Meta(BaseResource.Meta):
        identifier = 'place_orders'
        attributes = {
            'marketId': 'market_id',
            'status': 'status',
            'customerRef': 'customer_ref',
            'errorCode': 'error_code'
        }
        sub_resources = {
            'instructionReports': PlaceOrderInstructionReports
        }


class CancelOrderInstruction(BaseResource):
    """
    :type bet_id: unicode
    :type size_reduction: float
    """
    bet_id = None
    size_reduction = None

    class Meta(BaseResource.Meta):
        identifier = 'instruction'
        attributes = {
            'betId': 'bet_id',
            'sizeReduction': 'size_reduction'
        }


class CancelOrderInstructionReports(BaseResource):
    """
    :type cancelled_date: datetime.datetime
    :type error_code: str
    :type instruction: CancelOrderInstruction
    :type size_cancelled: float
    :type status: unicode
    """
    cancelled_date = None
    error_code = None
    instruction = None
    size_cancelled = None
    status = None

    class Meta(BaseResource.Meta):
        identifier = 'cancel_instruction_reports'
        attributes = {
            'status': 'status',
            'sizeCancelled': 'size_cancelled',
            'cancelledDate': 'cancelled_date',
            'errorCode': 'error_code',
        }
        sub_resources = {
            'instruction': CancelOrderInstruction
        }
        datetime_attributes = (
            'cancelledDate'
        )


class CancelOrders(BaseResource):
    """
    :type cancel_instruction_reports: list[CancelOrderInstructionReports]
    :type customer_ref: unicode
    :type error_code: str
    :type market_id: unicode
    :type status: unicode
    """
    cancel_instruction_reports = None
    customer_ref = None
    error_code = None
    market_id = None
    status = None

    class Meta(BaseResource.Meta):
        identifier = 'cancel_orders'
        attributes = {
            'marketId': 'market_id',
            'status': 'status',
            'customerRef': 'customer_ref',
            'errorCode': 'error_code'
        }
        sub_resources = {
            'instructionReports': CancelOrderInstructionReports
        }


class UpdateOrderInstruction(BaseResource):
    """
    :type bet_id: unicode
    :type new_persistence_type: unicode
    """
    bet_id = None
    new_persistence_type = None

    class Meta(BaseResource.Meta):
        identifier = 'instruction'
        attributes = {
            'betId': 'bet_id',
            'newPersistenceType': 'new_persistence_type'
        }


class UpdateOrderInstructionReports(BaseResource):
    """
    :type error_code: str
    :type instruction: UpdateOrderInstruction
    :type status: unicode
    """
    error_code = None
    instruction = None
    status = None

    class Meta(BaseResource.Meta):
        identifier = 'update_instruction_reports'
        attributes = {
            'status': 'status',
            'errorCode': 'error_code',
        }
        sub_resources = {
            'instruction': UpdateOrderInstruction
        }


class UpdateOrders(BaseResource):
    """
    :type customer_ref: unicode
    :type error_code: str
    :type market_id: unicode
    :type status: unicode
    :type update_instruction_reports: list[UpdateOrderInstructionReports]
    """
    customer_ref = None
    error_code = None
    market_id = None
    status = None
    update_instruction_reports = None

    class Meta(BaseResource.Meta):
        identifier = 'update_orders'
        attributes = {
            'marketId': 'market_id',
            'status': 'status',
            'customerRef': 'customer_ref',
            'errorCode': 'error_code'
        }
        sub_resources = {
            'instructionReports': UpdateOrderInstructionReports
        }


class ReplaceOrderInstructionReports(BaseResource):
    """
    :type cancel_instruction_reports: CancelOrderInstructionReports
    :type error_code: str
    :type place_instruction_reports: PlaceOrderInstructionReports
    :type status: unicode
    """
    cancel_instruction_reports = None
    error_code = None
    place_instruction_reports = None
    status = None

    class Meta(BaseResource.Meta):
        identifier = 'replace_instruction_reports'
        attributes = {
            'status': 'status',
            'errorCode': 'error_code',
        }
        sub_resources = {
            'cancelInstructionReport': CancelOrderInstructionReports,
            'placeInstructionReport': PlaceOrderInstructionReports
        }


class ReplaceOrders(BaseResource):
    """
    :type customer_ref: unicode
    :type error_code: str
    :type market_id: unicode
    :type replace_instruction_reports: list[ReplaceOrderInstructionReports]
    :type status: unicode
    """
    customer_ref = None
    error_code = None
    market_id = None
    replace_instruction_reports = None
    status = None

    class Meta(BaseResource.Meta):
        identifier = 'replace_orders'
        attributes = {
            'marketId': 'market_id',
            'status': 'status',
            'customerRef': 'customer_ref',
            'errorCode': 'error_code'
        }
        sub_resources = {
            'instructionReports': ReplaceOrderInstructionReports
        }
