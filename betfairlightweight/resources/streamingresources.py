import datetime

from .baseresource import BaseResource
from .bettingresources import MarketBook, CurrentOrders
from ..utils import strp_betfair_time, strp_betfair_integer_time
from ..enums import (
    StreamingOrderType, StreamingPersistenceType, StreamingSide, StreamingStatus
)


class BetfairModel:
    """ Base class for parsing betfair response """

    def __init__(self, date_time_sent, raw_response):
        """
        :param date_time_sent:
            Datetime request sent.
        :param raw_response:
            Raw response from requests.
        """
        self.date_time_received = datetime.datetime.utcnow()
        self.date_time_sent = date_time_sent
        self.raw_response = raw_response

    @property
    def elapsed_time(self):
        return (self.date_time_received-self.date_time_sent).total_seconds()

    def __str__(self):
        return self.__class__.__name__

    def __eq__(self, other):
        if self.raw_response == other.raw_response:
            return True


class MarketDefinition:

    def __init__(self, market_definition):
        self.bet_delay = market_definition.get('betDelay')
        self.betting_type = market_definition.get('bettingType')
        self.bsp_market = market_definition.get('bspMarket')
        self.bsp_reconciled = market_definition.get('bspReconciled')
        self.complete = market_definition.get('complete')
        self.country_code = market_definition.get('countryCode')
        self.cross_matching = market_definition.get('crossMatching')
        self.discount_allowed = market_definition.get('discountAllowed')
        self.event_id = market_definition.get('eventId')
        self.event_type_id = market_definition.get('eventId')
        self.in_play = market_definition.get('inPlay')
        self.market_base_rate = market_definition.get('marketBaseRate')
        self.market_time = strp_betfair_time(market_definition.get('marketTime'))
        self.market_type = market_definition.get('marketType')
        self.number_of_active_runners = market_definition.get('numberOfActiveRunners')
        self.number_of_winners = market_definition.get('numberOfWinners')
        self.open_date = strp_betfair_time(market_definition.get('openDate'))
        self.persistence_enabled = market_definition.get('persistenceEnabled')
        self.regulators = market_definition.get('regulators')
        self.runners = {runner.get('id'): MarketDefinitionRunner(runner)
                        for runner in market_definition.get('runners', [])}
        self.runners_voidable = market_definition.get('runnersVoidable')
        self.status = market_definition.get('status')
        self.suspend_time = strp_betfair_time(market_definition.get('suspendTime'))
        self.timezone = market_definition.get('timezone')
        self.turn_in_play_enabled = market_definition.get('turnInPlayEnabled')
        self.version = market_definition.get('version')


class MarketBookCache(BetfairModel):

    def __init__(self, date_time_sent, raw_response, market_book):
        super(MarketBookCache, self).__init__(date_time_sent, raw_response)
        self.date_updated = datetime.datetime.utcnow()
        self.market_id = market_book.get('id')
        self.image = market_book.get('img')
        self.total_matched = market_book.get('tv')
        self.market_definition = MarketDefinition(market_book.get('marketDefinition', {}))
        self.runners = {runner.get('id'): RunnerBook(runner) for runner in market_book.get('rc', [])}

    def update_cache(self, market_change):
        market_definition = market_change.get('marketDefinition')
        if market_definition:
            self.market_definition = MarketDefinition(market_definition)

        traded_volume = market_change.get('tv')
        if traded_volume:
            self.total_matched = traded_volume

        runner_change = market_change.get('rc')
        if runner_change:
            for new_data in runner_change:
                selection_id = new_data.get('id')
                runner = self.runners.get(selection_id)
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
                        runner.traded.update(new_data.get('trd'))
                    if new_data.get('atb'):
                        runner.atb.update_full_depth(new_data.get('atb'))
                    if new_data.get('atl'):
                        runner.atl.update_full_depth(new_data.get('atl'))
                    if new_data.get('batb'):
                        runner.atb.update_depth(new_data.get('batb'))
                    if new_data.get('batl'):
                        runner.atl.update_depth(new_data.get('batl'))
                    if new_data.get('bdatb'):
                        runner.atb.update_virtual_depth(new_data.get('bdatb'))
                    if new_data.get('bdatl'):
                        runner.atl.update_virtual_depth(new_data.get('bdatl'))
                else:
                    self.runners[new_data.get('id')] = RunnerBook(new_data)
        self.date_updated = datetime.datetime.utcnow()

    @property
    def create_market_book(self):
        return MarketBook(**self.serialise)

    @property
    def serialise(self):
        """Creates standard market book json response

        :return: Json market book object
        """
        return {'marketId': self.market_id,
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
                'runners': [runner.serialise(self.market_definition.runners.get(runner.selection_id).status)
                            for runner in self.runners.values()]
                }


class MarketDefinitionRunner:

    def __init__(self, runner):
        self.id = runner.get('id')
        self.sort_priority = runner.get('sortPriority')
        self.status = runner.get('status')


class RunnerBook:

    def __init__(self, runner_book):
        self.selection_id = runner_book.get('id')
        self.last_price_traded = runner_book.get('ltp')
        self.total_matched = runner_book.get('tv')
        self.traded = RunnerBookTraded(runner_book.get('trd'))
        self.atb = RunnerBookAvailableToBack(atb=runner_book.get('atb'),
                                             batb=runner_book.get('batb'),
                                             bdatb=runner_book.get('bdatb'))
        self.atl = RunnerBookAvailableToLay(atl=runner_book.get('atl'),
                                            batl=runner_book.get('batl'),
                                            bdatl=runner_book.get('bdatl'))
        self.spn = runner_book.get('spn')
        self.spf = runner_book.get('spf')

    def serialise(self, status):
        return {'status': status,
                'ex': {'tradedVolume': self.traded.traded_volume,
                       'availableToBack': self.atb.available_to_back,
                       'availableToLay': self.atl.available_to_lay},
                'adjustmentFactor': None,
                'lastPriceTraded': self.last_price_traded,
                'handicap': None,
                'totalMatched': self.total_matched,
                'selectionId': self.selection_id
                }


class RunnerBookTraded:

    def __init__(self, traded):
        self.traded = traded

    def update(self, traded_update):
        if not traded_update:
            print('empty ladder', traded_update)
            self.traded = traded_update
        for trade_update in traded_update:
            updated = False
            for (count, trade) in enumerate(self.traded):
                if trade[0] == trade_update[0]:
                    self.traded[count] = trade_update
                    updated = True
                    break
            if not updated:
                self.traded.append(trade_update)

    @property
    def traded_volume(self):
        if self.traded:
            return [{'price': volume[0], 'size': volume[1]}
                    for volume in sorted(self.traded, key=lambda x: x[0])]
        else:
            return []


class RunnerBookAvailableToBack:

    def __init__(self, atb=None, batb=None, bdatb=None):
        self.atb = atb
        self.batb = batb
        self.bdatb = bdatb

    def update_full_depth(self, book_update):
        if not self.atb:
            self.atb = book_update
        else:
            for book in book_update:
                updated = False
                if book[1] == 0:
                    for (count, trade) in enumerate(self.atb):
                        if trade[0] == book[0]:
                            del self.atb[count]
                            updated = True
                else:
                    for (count, trade) in enumerate(self.atb):
                        if trade[0] == book[0]:
                            self.atb[count] = book
                            updated = True
                            break
                if not updated:
                    self.atb.append(book)

    def update_depth(self, book_update):
        if not self.batb:
            self.batb = book_update
        else:
            for book in book_update:
                updated = False
                if book[2] == 0:
                    for (count, trade) in enumerate(self.batb):
                        if trade[0] == book[0]:
                            del self.batb[count]
                            updated = True
                else:
                    for (count, trade) in enumerate(self.batb):
                        if trade[0] == book[0]:
                            self.batb[count] = book
                            updated = True
                            break
                if not updated:
                    self.batb.append(book)

    def update_virtual_depth(self, book_update):
        if not self.bdatb:
            self.bdatb = book_update
        else:
            for book in book_update:
                updated = False
                for (count, trade) in enumerate(self.bdatb):
                    if trade[0] == book[0]:
                        self.bdatb[count] = book
                        updated = True
                        break
                if not updated:
                    self.bdatb.append(book)

    @property
    def available_to_back(self):
        if self.atb:
            return [{'price': volume[0], 'size': volume[1]}
                    for volume in sorted(self.atb, key=lambda x: x[0], reverse=True)]
        elif self.bdatb:
            return [{'price': volume[1], 'size': volume[2]}
                    for volume in sorted(self.bdatb, key=lambda x: x[0])]
        elif self.batb:
            return [{'price': volume[1], 'size': volume[2]}
                    for volume in sorted(self.batb, key=lambda x: x[0])]
        else:
            return []


class RunnerBookAvailableToLay:

    def __init__(self, atl=None, batl=None, bdatl=None):
        self.atl = atl
        self.batl = batl
        self.bdatl = bdatl

    def update_full_depth(self, book_update):
        if not self.atl:
            self.atl = book_update
        else:
            for book in book_update:
                updated = False
                if book[1] == 0:
                    for (count, trade) in enumerate(self.atl):
                        if trade[0] == book[0]:
                            del self.atl[count]
                            updated = True
                else:
                    for (count, trade) in enumerate(self.atl):
                        if trade[0] == book[0]:
                            self.atl[count] = book
                            updated = True
                            break
                if not updated:
                    self.atl.append(book)

    def update_depth(self, book_update):
        if not self.batl:
            self.batl = book_update
        else:
            for book in book_update:
                updated = False
                if book[2] == 0:
                    for (count, trade) in enumerate(self.batl):
                        if trade[0] == book[0]:
                            del self.batl[count]
                            updated = True
                else:
                    for (count, trade) in enumerate(self.batl):
                        if trade[0] == book[0]:
                            self.batl[count] = book
                            updated = True
                            break
                if not updated:
                    self.batl.append(book)

    def update_virtual_depth(self, book_update):
        if not self.bdatl:
            self.bdatl = book_update
        else:
            for book in book_update:
                updated = False
                for (count, trade) in enumerate(self.bdatl):
                    if trade[0] == book[0]:
                        self.bdatl[count] = book
                        updated = True
                        break
                if not updated:
                    self.bdatl.append(book)

    @property
    def available_to_lay(self):
        if self.atl:
            return [{'price': volume[0], 'size': volume[1]}
                    for volume in sorted(self.atl, key=lambda x: x[0])]
        elif self.bdatl:
            return [{'price': volume[1], 'size': volume[2]}
                    for volume in sorted(self.bdatl, key=lambda x: x[0])]
        elif self.batl:
            return [{'price': volume[1], 'size': volume[2]}
                    for volume in sorted(self.batl, key=lambda x: x[0])]
        return []


class OrderBookCache(BetfairModel):

    def __init__(self, date_time_sent, raw_response, order_book):
        super(OrderBookCache, self).__init__(date_time_sent, raw_response)
        self.date_updated = datetime.datetime.utcnow()
        self.market_id = order_book.get('id')
        self.closed = order_book.get('closed')
        self.runners = {order_changes.get('id'): OrderBookRunner(order_changes, self.market_id)
                        for order_changes in order_book.get('orc')}

    def update_cache(self, order_book):
        self.date_updated = datetime.datetime.utcnow()
        for order_changes in order_book.get('orc'):
            selection_id = order_changes['id']
            runner = self.runners.get(selection_id)
            if runner:
                runner.update_matched_lays(order_changes.get('ml', []))
                runner.update_unmatched_backs(order_changes.get('mb', []))
                runner.update_unmatched(order_changes.get('uo', []))
            else:
                self.runners[order_changes.get('id')] = OrderBookRunner(order_changes, self.market_id)

    @property
    def serialise(self):
        orders = []
        for runner in self.runners.values():
            orders.extend(runner.serialise_orders)
        return {"currentOrders": orders,
                "moreAvailable": False}

    @property
    def create_order_book(self):
        return CurrentOrders(**self.serialise)


class OrderBookRunner:

    def __init__(self, order_changes, market_id):
        self.selection_id = order_changes.get('id')
        self.market_id = market_id
        self.matched_lays = [Match(matched) for matched in order_changes.get('ml', [])]
        self.matched_backs = [Match(matched) for matched in order_changes.get('mb', [])]
        self.unmatched_orders = {unmatched_order.get('id'): UnmatchedOrder(unmatched_order)
                                 for unmatched_order in order_changes.get('uo', [])}

    def update_matched_lays(self, matched_lays):
        for matched_lay in matched_lays:
            updated = False
            (price, size) = matched_lay
            for matches in self.matched_lays:
                if matches.price == price:
                    matches.size = size
                    updated = True
                    break
            if not updated:
                self.matched_lays.append(Match(matched_lay))

    def update_unmatched_backs(self, matched_backs):
        for matched_back in matched_backs:
            updated = False
            (price, size) = matched_back
            for matches in self.matched_backs:
                if matches.price == price:
                    matches.size = size
                    updated = True
                    break
            if not updated:
                self.matched_backs.append(Match(matched_back))

    def update_unmatched(self, unmatched_orders):
        for unmatched_order in unmatched_orders:
            self.unmatched_orders[unmatched_order.get('id')] = UnmatchedOrder(unmatched_order)

    @property
    def serialise_orders(self):
        return [order.serialise(self.market_id, self.selection_id) for order in self.unmatched_orders.values()]


class Match:

    def __init__(self, matched):
        self.price = matched[0]
        self.size = matched[1]


class UnmatchedOrder:

    def __init__(self, unmatched_order):
        self.bet_id = unmatched_order.get('id')
        self.price = unmatched_order.get('p')
        self.size = unmatched_order.get('s')
        self.bsp_liability = unmatched_order.get('bsp', 0.0)
        self.side = unmatched_order.get('side')
        self.status = unmatched_order.get('status')
        self.persistence_type = unmatched_order.get('pt')
        self.order_type = unmatched_order.get('ot')
        self.placed_date = strp_betfair_integer_time(unmatched_order.get('pd'))
        self.matched_date = strp_betfair_integer_time(unmatched_order.get('md'))
        self.average_price_matched = unmatched_order.get('avp', 0.0)
        self.size_matched = unmatched_order.get('sm')
        self.size_remaining = unmatched_order.get('sr')
        self.size_lapsed = unmatched_order.get('sl')
        self.size_cancelled = unmatched_order.get('sc')
        self.size_voided = unmatched_order.get('sv')
        self.regulator_auth_code = unmatched_order.get('rac')
        self.regulator_code = unmatched_order.get('rc')

    def serialise(self, market_id, selection_id):
        return {"averagePriceMatched": self.average_price_matched,
                "betId": self.bet_id,
                "bspLiability": self.bsp_liability,
                "handicap": 0.0,
                "marketId": market_id,
                "orderType": StreamingOrderType[self.order_type].value,
                "persistenceType": StreamingPersistenceType[self.persistence_type].value,
                "placedDate": self.placed_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "priceSize": {
                    "price": self.price,
                    "size": self.size
                },
                "regulatorCode": self.regulator_code,
                "selectionId": selection_id,
                "side": StreamingSide[self.side].value,
                "sizeCancelled": self.size_cancelled,
                "sizeLapsed": self.size_lapsed,
                "sizeMatched": self.size_matched,
                "sizeRemaining": self.size_remaining,
                "sizeVoided": self.size_voided,
                "status": StreamingStatus[self.status].value}
