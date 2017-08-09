import datetime

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

    def __init__(self, id, sortPriority, status, hc=None, bsp=None, adjustmentFactor=None, removalDate=None, name=None):
        self.selection_id = id
        self.sort_priority = sortPriority
        self.status = status
        self.handicap = hc
        self.bsp = bsp
        self.adjustment_factor = adjustmentFactor
        self.removal_date = BaseResource.strip_datetime(removalDate)
        self.name = name  # historic data only

    def __str__(self):
        return 'MarketDefinitionRunner: %s' % self.selection_id

    def __repr__(self):
        return '<MarketDefinitionRunner>'


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
                 suspendTime=None, marketType=None, lineMaxUnit=None, lineMinUnit=None, lineInterval=None, name=None,
                 eventName=None, priceLadderDefinition=None, keyLineDefinition=None):
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
        self.runners = [
            MarketDefinitionRunner(**i) for i in runners
        ]
        self.name = name  # historic data only
        self.event_name = eventName  # historic data only
        self.runners_dict = {
            (runner.selection_id, runner.handicap): runner for runner in self.runners
        }
        self.price_ladder_definition = priceLadderDefinition
        self.key_line_definition = keyLineDefinition


class Available(object):
    """
    Data structure to hold prices/traded amount,
    designed to be as quick as possible.
    """

    def __init__(self, prices, deletion_select, reverse=False):
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

    def sort(self):
        self.prices.sort(reverse=self.reverse)
        self.serialise = [
            {'price': volume[self.deletion_select-1], 'size': volume[self.deletion_select]} for volume in self.prices
        ]

    def clear(self):
        self.prices = []
        self.sort()

    def update(self, book_update):
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
                    # handles betfair bug, http://forum.bdp.betfair.com/showthread.php?t=3351
                    self.prices.append(book)
        self.sort()


class RunnerBook(object):

    def __init__(self, id, ltp=None, tv=None, trd=None, atb=None, batb=None, bdatb=None, atl=None, batl=None,
                 bdatl=None, spn=None, spf=None, spb=None, spl=None, hc=None):
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

    def update_traded(self, traded_update):
        """:param traded_update: [price, size]
        """
        if not traded_update:
            self.traded.clear()
        else:
            self.traded.update(traded_update)

    def serialise_available_to_back(self):
        if self.available_to_back.prices:
            return self.available_to_back.serialise
        elif self.best_display_available_to_back.prices:
            return self.best_display_available_to_back.serialise
        elif self.best_available_to_back.prices:
            return self.best_available_to_back.serialise
        else:
            return []

    def serialise_available_to_lay(self):
        if self.available_to_lay.prices:
            return self.available_to_lay.serialise
        elif self.best_display_available_to_lay.prices:
            return self.best_display_available_to_lay.serialise
        elif self.best_available_to_lay.prices:
            return self.best_available_to_lay.serialise
        return []

    def serialise(self, runner_definition):
        return {
            'status': runner_definition.status,
            'ex': {
                'tradedVolume': self.traded.serialise,
                'availableToBack': self.serialise_available_to_back(),
                'availableToLay': self.serialise_available_to_lay()
            },
            'sp': {
                'nearPrice': self.starting_price_near,
                'farPrice': self.starting_price_far,
                'backStakeTaken': self.starting_price_back.serialise,
                'layLiabilityTaken': self.starting_price_lay.serialise,
                'actualSP': runner_definition.bsp
            },
            'adjustmentFactor': runner_definition.adjustment_factor,
            'removalDate': runner_definition.removal_date,
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
        self.market_definition = MarketDefinition(**kwargs['marketDefinition']) if \
            'marketDefinition' in kwargs else None
        self.runners = [RunnerBook(**i) for i in kwargs.get('rc', [])]

    def update_cache(self, market_change, publish_time):
        self._datetime_updated = self.strip_datetime(publish_time)
        self.publish_time = publish_time

        if 'marketDefinition' in market_change:
            self.market_definition = MarketDefinition(**market_change['marketDefinition'])

        if 'tv' in market_change:
            self.total_matched = market_change['tv']

        if 'rc' in market_change:
            for new_data in market_change['rc']:
                runner = self.runner_dict.get(
                    (new_data['id'], new_data.get('hc'))
                )
                if runner:
                    if 'ltp' in new_data:
                        runner.last_price_traded = new_data['ltp']
                    if 'tv' in new_data:  # if runner removed tv: 0 is returned
                        runner.total_matched = new_data['tv']
                    if 'spn' in new_data:
                        runner.starting_price_near = new_data['spn']
                    if 'spf' in new_data:
                        runner.starting_price_far = new_data['spf']
                    if 'trd' in new_data:
                        runner.update_traded(new_data['trd'])
                    if 'atb' in new_data:
                        runner.available_to_back.update(new_data['atb'])
                    if 'atl' in new_data:
                        runner.available_to_lay.update(new_data['atl'])
                    if 'batb' in new_data:
                        runner.best_available_to_back.update(new_data['batb'])
                    if 'batl' in new_data:
                        runner.best_available_to_lay.update(new_data['batl'])
                    if 'bdatb' in new_data:
                        runner.best_display_available_to_back.update(new_data['bdatb'])
                    if 'bdatl' in new_data:
                        runner.best_display_available_to_lay.update(new_data['bdatl'])
                    if 'spb' in new_data:
                        runner.starting_price_back.update(new_data['spb'])
                    if 'spl' in new_data:
                        runner.starting_price_lay.update(new_data['spl'])
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
        return {(runner.selection_id, runner.handicap): runner for runner in self.runners}

    @property
    def serialise(self):
        """Creates standard market book json response,
        will error if EX_MARKET_DEF not incl.
        """
        return {
            'marketId': self.market_id,
            'totalAvailable': None,
            'isMarketDataDelayed': None,
            'lastMatchTime': None,
            'betDelay': self.market_definition.bet_delay,
            'version': self.market_definition.version,
            'complete': self.market_definition.complete,
            'runnersVoidable': self.market_definition.runners_voidable,
            'totalMatched': self.total_matched,
            'status': self.market_definition.status,
            'bspReconciled': self.market_definition.bsp_reconciled,
            'crossMatching': self.market_definition.cross_matching,
            'inplay': self.market_definition.in_play,
            'numberOfWinners': self.market_definition.number_of_winners,
            'numberOfRunners': len(self.market_definition.runners),
            'numberOfActiveRunners': self.market_definition.number_of_active_runners,
            'runners': [
                runner.serialise(
                    self.market_definition.runners_dict[(runner.selection_id, runner.handicap)]
                ) for runner in self.runners
            ],
            'publishTime': self.publish_time,
        }


class UnmatchedOrder(object):

    def __init__(self, id, p, s, side, status, ot, pd, sm, sr, sl, sc, sv, rfo, rfs, pt=None,
                 md=None, avp=None, bsp=None, ld=None, rac=None, rc=None):
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
        self.lapsed_date = ld

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
            'persistenceType': StreamingPersistenceType[self.persistence_type].value if self.persistence_type else None,
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

    def __init__(self, id, fullImage=None, ml=None, mb=None, uo=None, hc=None, smc=None):
        self.selection_id = id
        self.full_image = fullImage
        self.matched_lays = Available(ml, 1)
        self.matched_backs = Available(mb, 1)
        self.unmatched_orders = [UnmatchedOrder(**i) for i in uo] if uo else []
        self.handicap = hc
        self.strategy_matches = smc

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
        return [
            order.serialise(market_id, self.selection_id) for order in self.unmatched_orders
        ]


class OrderBookCache(BaseResource):

    def __init__(self, **kwargs):
        super(OrderBookCache, self).__init__(**kwargs)
        self.publish_time = kwargs.get('publish_time')
        self.market_id = kwargs.get('id')
        self.closed = kwargs.get('closed')
        self.runners = [OrderBookRunner(**i) for i in kwargs.get('orc', [])]

    def update_cache(self, order_book, publish_time):
        self._datetime_updated = self.strip_datetime(publish_time)
        self.publish_time = publish_time

        for order_changes in order_book.get('orc', []):
            selection_id = order_changes['id']
            runner = self.runner_dict.get(selection_id)
            if runner:
                if 'ml' in order_changes:
                    runner.matched_lays.update(order_changes['ml'])
                if 'mb' in order_changes:
                    runner.matched_backs.update(order_changes['mb'])
                if 'uo' in order_changes:
                    runner.update_unmatched(order_changes['uo'])
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
                publish_time=self.publish_time,
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
