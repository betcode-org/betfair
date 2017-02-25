from operator import itemgetter

from ..utils import update_available
from .baseresource import BaseResource
from .bettingresources import (
    MarketBook,
    CurrentOrders,
)
from ..enums import (
    StreamingOrderType,
    StreamingPersistenceType,
    StreamingSide,
    StreamingStatus,
)


class MarketDefinitionRunner(BaseResource):
    """
    :type adjustment_factor: float
    :type id: int
    :type removal_date: datetime.datetime
    :type sort_priority: int
    :type status: unicode
    """
    adjustment_factor = None
    id = None
    removal_date = None
    sort_priority = None
    status = None

    class Meta(BaseResource.Meta):
        identifier = 'runners'
        attributes = {
            'id': 'id',
            'sortPriority': 'sort_priority',
            'status': 'status',
            'adjustmentFactor': 'adjustment_factor',
            'removalDate': 'removal_date',
        }
        datetime_attributes = (
            'removalDate',
        )


class MarketDefinition(BaseResource):
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
    :type market_base_rate: int
    :type market_time: datetime.datetime
    :type market_type: unicode
    :type number_of_active_runners: int
    :type number_of_winners: int
    :type open_date: datetime.datetime
    :type persistence_enabled: bool
    :type regulators: list[unicode]
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
    bet_delay = None
    betting_type = None
    bsp_market = None
    bsp_reconciled = None
    complete = None
    country_code = None
    cross_matching = None
    discount_allowed = None
    event_id = None
    event_type_id = None
    in_play = None
    market_base_rate = None
    market_time = None
    market_type = None
    number_of_active_runners = None
    number_of_winners = None
    open_date = None
    persistence_enabled = None
    regulators = None
    runners = None
    runners_voidable = None
    settled_time = None
    status = None
    suspend_time = None
    timezone = None
    turn_in_play_enabled = None
    venue = None
    version = None

    class Meta(BaseResource.Meta):
        identifier = 'market_definition'
        attributes = {
            'betDelay': 'bet_delay',
            'bettingType': 'betting_type',
            'bspMarket': 'bsp_market',
            'bspReconciled': 'bsp_reconciled',
            'complete': 'complete',
            'countryCode': 'country_code',
            'crossMatching': 'cross_matching',
            'discountAllowed': 'discount_allowed',
            'eventId': 'event_id',
            'eventTypeId': 'event_type_id',
            'inPlay': 'in_play',
            'marketBaseRate': 'market_base_rate',
            'marketTime': 'market_time',
            'marketType': 'market_type',
            'numberOfActiveRunners': 'number_of_active_runners',
            'numberOfWinners': 'number_of_winners',
            'persistenceEnabled': 'persistence_enabled',
            'regulators': 'regulators',
            'runnersVoidable': 'runners_voidable',
            'settledTime': 'settled_time',
            'openDate': 'open_date',
            'status': 'status',
            'suspendTime': 'suspend_time',
            'venue': 'venue',
            'timezone': 'timezone',
            'turnInPlayEnabled': 'turn_in_play_enabled',
            'version': 'version',
        }
        sub_resources = {
            'runners': MarketDefinitionRunner
        }
        datetime_attributes = (
            'marketTime',
            'openDate',
            'suspendTime',
            'settledTime',
        )


class RunnerBook(BaseResource):
    class Meta(BaseResource.Meta):
        identifier = 'runners'
        attributes = {
            'id': 'selection_id',
            'ltp': 'last_price_traded',
            'tv': 'total_matched',
            'trd': 'traded',
            'atb': 'available_to_back',
            'batb': 'best_available_to_back',
            'bdatb': 'best_display_available_to_back',
            'atl': 'available_to_lay',
            'batl': 'best_available_to_lay',
            'bdatl': 'best_display_available_to_lay',
            'spn': 'starting_price_near',
            'spf': 'starting_price_far',
            'spb': 'starting_price_back',
            'spl': 'starting_price_lay',
        }

    def update_traded(self, traded_update):
        """:param traded_update: price, size
        """
        if not traded_update:
            self.traded = traded_update
        elif not self.traded:
            self.traded = traded_update
        else:
            update_available(self.traded, traded_update, 1)

    def update_available_to_back(self, book_update):
        """:param book_update: price, size
        """
        if not self.available_to_back:
            self.available_to_back = book_update
        else:
            update_available(self.available_to_back, book_update, 1)

    def update_available_to_lay(self, book_update):
        """:param book_update: price, size
        """
        if not self.available_to_lay:
            self.available_to_lay = book_update
        else:
            update_available(self.available_to_lay, book_update, 1)

    def update_best_available_to_back(self, book_update):
        """:param book_update: level, price, size
        """
        if not self.best_available_to_back:
            self.best_available_to_back = book_update
        else:
            update_available(self.best_available_to_back, book_update, 2)

    def update_best_available_to_lay(self, book_update):
        """:param book_update: level, price, size
        """
        if not self.best_available_to_lay:
            self.best_available_to_lay = book_update
        else:
            update_available(self.best_available_to_lay, book_update, 2)

    def update_best_display_available_to_back(self, book_update):
        """:param book_update: level, price, size
        """
        if not self.best_display_available_to_back:
            self.best_display_available_to_back = book_update
        else:
            update_available(self.best_display_available_to_back, book_update, 2)

    def update_best_display_available_to_lay(self, book_update):
        """:param book_update: level, price, size
        """
        if not self.best_display_available_to_lay:
            self.best_display_available_to_lay = book_update
        else:
            update_available(self.best_display_available_to_lay, book_update, 2)

    def update_starting_price_back(self, book_update):
        """:param book_update: price, size
        """
        if not self.starting_price_back:
            self.starting_price_back = book_update
        else:
            update_available(self.starting_price_back, book_update, 1)

    def update_starting_price_lay(self, book_update):
        """:param book_update: price, size
        """
        if not self.starting_price_lay:
            self.starting_price_lay = book_update
        else:
            update_available(self.starting_price_lay, book_update, 1)

    @property
    def serialise_traded_volume(self):
        if self.traded:
            return [{'price': volume[0], 'size': volume[1]}
                    for volume in sorted(self.traded, key=itemgetter(0))]
        else:
            return []

    @property
    def serialise_available_to_back(self):
        if self.available_to_back:
            return [{'price': volume[0], 'size': volume[1]}
                    for volume in sorted(self.available_to_back, key=itemgetter(0), reverse=True)]
        elif self.best_display_available_to_back:
            return [{'price': volume[1], 'size': volume[2]}
                    for volume in sorted(self.best_display_available_to_back, key=itemgetter(0))]
        elif self.best_available_to_back:
            return [{'price': volume[1], 'size': volume[2]}
                    for volume in sorted(self.best_available_to_back, key=itemgetter(0))]
        else:
            return []

    @property
    def serialise_available_to_lay(self):
        if self.available_to_lay:
            return [{'price': volume[0], 'size': volume[1]}
                    for volume in sorted(self.available_to_lay, key=itemgetter(0))]
        elif self.best_display_available_to_lay:
            return [{'price': volume[1], 'size': volume[2]}
                    for volume in sorted(self.best_display_available_to_lay, key=itemgetter(0))]
        elif self.best_available_to_lay:
            return [{'price': volume[1], 'size': volume[2]}
                    for volume in sorted(self.best_available_to_lay, key=itemgetter(0))]
        return []

    def serialise(self, status):
        return {
            'status': status,
            'ex': {
                'tradedVolume': self.serialise_traded_volume,
                'availableToBack': self.serialise_available_to_back,
                'availableToLay': self.serialise_available_to_lay
            },
            'adjustmentFactor': None,
            'lastPriceTraded': self.last_price_traded,
            'handicap': None,
            'totalMatched': self.total_matched,
            'selectionId': self.selection_id
        }


class MarketBookCache(BaseResource):

    class Meta(BaseResource.Meta):
        identifier = 'market_book_cache'
        attributes = {
            'id': 'market_id',
            'img': 'image',
            'tv': 'total_matched'
        }
        sub_resources = {
            'marketDefinition': MarketDefinition,
            'rc': RunnerBook
        }

    def update_cache(self, market_change, publish_time):
        self._datetime_updated = self.strip_datetime(publish_time)
        self.publish_time = publish_time

        market_definition = market_change.get('marketDefinition')
        if market_definition:
            self.market_definition = MarketDefinition(**market_definition)

        traded_volume = market_change.get('tv')
        if traded_volume:
            self.total_matched = traded_volume

        runner_change = market_change.get('rc')
        if runner_change:
            for new_data in runner_change:
                selection_id = new_data.get('id')
                runner = self.runner_dict.get(selection_id)
                if runner:
                    if new_data.get('ltp'):
                        runner.last_price_traded = new_data.get('ltp')
                    if new_data.get('tv'):
                        runner.total_matched = new_data.get('tv')
                    if new_data.get('spn'):
                        runner.spn = new_data.get('spn')
                    if new_data.get('spf'):
                        runner.spf = new_data.get('spf')
                    if new_data.get('trd'):
                        runner.update_traded(new_data.get('trd'))
                    if new_data.get('atb'):
                        runner.update_available_to_back(new_data.get('atb'))
                    if new_data.get('atl'):
                        runner.update_available_to_lay(new_data.get('atl'))
                    if new_data.get('batb'):
                        runner.update_best_available_to_back(new_data.get('batb'))
                    if new_data.get('batl'):
                        runner.update_best_available_to_lay(new_data.get('batl'))
                    if new_data.get('bdatb'):
                        runner.update_best_display_available_to_back(new_data.get('bdatb'))
                    if new_data.get('bdatl'):
                        runner.update_best_display_available_to_lay(new_data.get('bdatl'))
                    if new_data.get('spb'):
                        runner.update_starting_price_back(new_data.get('spb'))
                    if new_data.get('spl'):
                        runner.update_starting_price_back(new_data.get('spl'))
                else:
                    self.runners.append(RunnerBook(**new_data))

    def create_market_book(self, unique_id):
        return MarketBook(
            date_time_sent=self._datetime_updated,
            streaming_unique_id=unique_id,
            market_definition=self.market_definition,
            **self.serialise
        )

    @property
    def runner_dict(self):
        return {runner.selection_id: runner for runner in self.runners}

    @property
    def market_definition_dict(self):
        return {runner.id: runner for runner in self.market_definition.runners}

    @property
    def serialise(self):
        """Creates standard market book json response,
        will error if EX_MARKET_DEF not incl.
        """
        return {
            'marketId': self.market_id,
            'totalAvailable': None,
            'betDelay': self.market_definition.bet_delay,
            'version': self.market_definition.version,
            'complete': self.market_definition.complete,
            'numberOfRunners': None,
            'runnersVoidable': self.market_definition.runners_voidable,
            'totalMatched': self.total_matched,
            'status': self.market_definition.status,
            'bspReconciled': self.market_definition.bsp_reconciled,
            'isMarketDataDelayed': None,
            'lastMatchTime': None,
            'crossMatching': self.market_definition.cross_matching,
            'inplay': self.market_definition.in_play,
            'numberOfWinners': self.market_definition.number_of_winners,
            'numberOfActiveRunners': self.market_definition.number_of_active_runners,
            'runners': [runner.serialise(self.market_definition_dict.get(runner.selection_id).status)
                        for runner in self.runners],
            'publishTime': self.publish_time,
        }


class UnmatchedOrder(BaseResource):

    class Meta(BaseResource.Meta):
        identifier = 'unmatched_orders'
        attributes = {
            'id': 'bet_id',
            'p': 'price',
            's': 'size',
            'bsp': 'bsp_liability',
            'side': 'side',
            'status': 'status',
            'pt': 'persistence_type',
            'ot': 'order_type',
            'pd': 'placed_date',
            'md': 'matched_date',
            'avp': 'average_price_matched',
            'sm': 'size_matched',
            'sr': 'size_remaining',
            'sl': 'size_lapsed',
            'sc': 'size_cancelled',
            'sv': 'size_voided',
            'rac': 'regulator_auth_code',
            'rc': 'regulator_code',
            'rfo': 'reference_order',
            'rfs': 'reference_strategy',
        }
        datetime_attributes = (
            'pd',
            'md'
        )

    def serialise(self, market_id, selection_id):
        return {
            'averagePriceMatched': self.average_price_matched or 0.0,
            'betId': self.bet_id,
            'bspLiability': self.bsp_liability,
            'handicap': 0.0,
            'marketId': market_id,
            'matchedDate': self.matched_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ') if self.matched_date is not None else self.matched_date,
            'orderType': StreamingOrderType[self.order_type].value,
            'persistenceType': StreamingPersistenceType[self.persistence_type].value,
            'placedDate': self.placed_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'priceSize': {
                'price': self.price,
                'size': self.size
            },
            'regulatorCode': self.regulator_code,
            'selectionId': selection_id,
            'side': StreamingSide[self.side].value,
            'sizeCancelled': self.size_cancelled,
            'sizeLapsed': self.size_lapsed,
            'sizeMatched': self.size_matched,
            'sizeRemaining': self.size_remaining,
            'sizeVoided': self.size_voided,
            'status': StreamingStatus[self.status].value,
            'customerStrategyRef': self.reference_strategy,
            'customerOrderRef': self.reference_order,
        }


class OrderBookRunner(BaseResource):

    class Meta(BaseResource.Meta):
        identifier = 'runners'
        attributes = {
            'id': 'selection_id',
            'ml': 'matched_lays',
            'mb': 'matched_backs',
        }
        sub_resources = {
            'uo': UnmatchedOrder
        }

    def update_matched_backs(self, matched_backs):
        if not self.matched_backs:
            self.matched_backs = [matched_back for matched_back in matched_backs]
        else:
            update_available(self.matched_backs, matched_backs, 1)

    def update_matched_lays(self, matched_lays):
        if not self.matched_lays:
            self.matched_lays = [matched_lay for matched_lay in matched_lays]
        else:
            update_available(self.matched_lays, matched_lays, 1)

    def update_unmatched(self, unmatched_orders):
        order_dict = {order.bet_id: order for order in self.unmatched_orders}
        for unmatched_order in unmatched_orders:
            if unmatched_order.get('id') in order_dict:
                for n, order in enumerate(self.unmatched_orders):
                    if order.bet_id == unmatched_order.get('id'):
                        self.unmatched_orders[n] = UnmatchedOrder(**unmatched_order)
                        break
            else:
                self.unmatched_orders.append(UnmatchedOrder(**unmatched_order))

    def serialise_orders(self, market_id):
        return [order.serialise(market_id, self.selection_id) for order in self.unmatched_orders]


class OrderBookCache(BaseResource):

    class Meta(BaseResource.Meta):
        identifier = 'order_book_cache'
        attributes = {
            'id': 'market_id',
            'closed': 'closed'
        }
        sub_resources = {
            'orc': OrderBookRunner
        }

    def update_cache(self, order_book, publish_time):
        self._datetime_updated = self.strip_datetime(publish_time)

        for order_changes in order_book.get('orc', []):
            selection_id = order_changes.get('id')
            runner = self.runner_dict.get(selection_id)
            if runner:
                runner.update_matched_lays(order_changes.get('ml', []))
                runner.update_matched_backs(order_changes.get('mb', []))
                runner.update_unmatched(order_changes.get('uo', []))
            else:
                self.runners.append(OrderBookRunner(**order_changes))

    def create_order_book(self, unique_id):
        return CurrentOrders(date_time_sent=self._datetime_updated, streaming_unique_id=unique_id, **self.serialise)

    @property
    def runner_dict(self):
        return {runner.selection_id: runner for runner in self.runners}

    @property
    def serialise(self):
        orders = []
        for runner in self.runners:
            orders.extend(runner.serialise_orders(self.market_id))
        return {
            'currentOrders': orders,
            'moreAvailable': False
        }
