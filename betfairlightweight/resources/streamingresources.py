import datetime
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


class MarketDefinitionRunner(object):
    """
    :type adjustment_factor: float
    :type id: int
    :type removal_date: datetime.datetime
    :type sort_priority: int
    :type status: unicode
    """

    def __init__(self, id, sortPriority, status, hc=None, bsp=None, adjustmentFactor=None, removalDate=None):
        self.id = id
        self.sort_priority = sortPriority
        self.status = status
        self.handicap = hc
        self.bsp = bsp
        self.adjustment_factor = adjustmentFactor
        self.removal_date = BaseResource.strip_datetime(removalDate)


class MarketDefinition(object):
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

    def __init__(self, betDelay, bettingType, bspMarket, bspReconciled, complete, crossMatching, discountAllowed,
                 eventId, eventTypeId, inPlay, marketBaseRate, marketTime, numberOfActiveRunners, numberOfWinners,
                 openDate, persistenceEnabled, regulators, runnersVoidable, status, timezone, turnInPlayEnabled,
                 version, runners, countryCode=None, eachWayDivisor=None, venue=None, settledTime=None,
                 suspendTime=None, marketType=None, lineMaxUnit=None, lineMinUnit=None, lineInterval=None):
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
        self.open_date = BaseResource.strip_datetime(openDate)
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


class RunnerBook(object):

    def __init__(self, id, ltp=None, tv=None, trd=None, atb=None, batb=None, bdatb=None, atl=None, batl=None,
                 bdatl=None, spn=None, spf=None, spb=None, spl=None, hc=None):
        self.selection_id = id
        self.last_price_traded = ltp
        self.total_matched = tv
        self.traded = trd
        self.available_to_back = atb
        self.best_available_to_back = batb
        self.best_display_available_to_back = bdatb
        self.available_to_lay = atl
        self.best_available_to_lay = batl
        self.best_display_available_to_lay = bdatl
        self.starting_price_near = spn
        self.starting_price_far = spf
        self.starting_price_back = spb
        self.starting_price_lay = spl
        self.handicap = hc

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
            'handicap': self.handicap,
            'totalMatched': self.total_matched,
            'selectionId': self.selection_id
        }


class MarketBookCache(BaseResource):

    def __init__(self, **kwargs):
        super(MarketBookCache, self).__init__(**kwargs)
        self.publish_time = kwargs.get('publish_time')
        self.market_id = kwargs.get('id')
        self.image = kwargs.get('img')
        self.total_matched = kwargs.get('tv')
        self.market_definition = MarketDefinition(**kwargs.get('marketDefinition')) if \
            kwargs.get('marketDefinition') else None
        self.runners = [RunnerBook(**i) for i in kwargs.get('rc', [])]

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

    def create_market_book(self, unique_id, streaming_update, lightweight):
        if lightweight:
            return self.serialise
        else:
            return MarketBook(
                elapsed_time=(datetime.datetime.utcnow()-self._datetime_updated).total_seconds(),
                streaming_unique_id=unique_id,
                streaming_update=streaming_update,
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


class UnmatchedOrder(object):

    def __init__(self, id, p, s, side, status, pt, ot, pd, sm, sr, sl, sc, sv, rac, rc, rfo, rfs,
                 md=None, avp=None, bsp=None):
        self.bet_id = id
        self.price = p
        self.size = s
        self.bsp_liability = bsp
        self.side = side
        self.status = status
        self.persistence_type = pt
        self.order_type = ot
        self.placed_date = BaseResource.strip_datetime(pd)
        self.matched_date = BaseResource.strip_datetime(md)
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

    def serialise(self, market_id, selection_id):
        return {
            'averagePriceMatched': self.average_price_matched or 0.0,
            'betId': self.bet_id,
            'bspLiability': self.bsp_liability,
            'handicap': 0.0,
            'marketId': market_id,
            'matchedDate': self.matched_date.strftime(
                '%Y-%m-%dT%H:%M:%S.%fZ') if self.matched_date is not None else self.matched_date,
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


class OrderBookRunner(object):

    def __init__(self, id, fullImage=None, ml=None, mb=None, uo=None):
        self.selection_id = id
        self.full_image = fullImage
        self.matched_lays = ml
        self.matched_backs = mb
        self.unmatched_orders = [UnmatchedOrder(**i) for i in uo] if uo else []

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

    def __init__(self, **kwargs):
        super(OrderBookCache, self).__init__(**kwargs)
        self.market_id = kwargs.get('id')
        self.closed = kwargs.get('closed')
        self.runners = [OrderBookRunner(**i) for i in kwargs.get('orc', [])]

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

    def create_order_book(self, unique_id, streaming_update, lightweight):
        if lightweight:
            return self.serialise
        else:
            return CurrentOrders(
                elapsed_time=(datetime.datetime.utcnow()-self._datetime_updated).total_seconds(),
                streaming_unique_id=unique_id,
                streaming_update=streaming_update,
                **self.serialise
            )

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
