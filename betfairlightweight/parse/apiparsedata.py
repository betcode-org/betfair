import datetime

from ..parse.models import BetfairModel
from ..utils import strp_betfair_time, price_check


class EventType:

    def __init__(self, event_type):
        self.id = event_type.get('id')
        self.name = event_type.get('name')


class EventTypeResult(BetfairModel):

    def __init__(self, date_time_sent, raw_response, event_type):
        super(EventTypeResult, self).__init__(date_time_sent, raw_response)
        self.market_count = event_type.get('marketCount')
        self.event_type = EventType(event_type.get('eventType'))


class CompetitionResult(BetfairModel):

    def __init__(self, date_time_sent, raw_response, competition):
        super(CompetitionResult, self).__init__(date_time_sent, raw_response)
        self.market_count = competition.get('marketCount')
        self.competition_region = competition.get('competitionRegion')
        self.competition = EventType(competition.get('competition'))


class TimeRange:

    def __init__(self, time_range):
        self._from = strp_betfair_time(time_range.get('from'))
        self.to = strp_betfair_time(time_range.get('to'))


class TimeRangeResult(BetfairModel):

    def __init__(self, date_time_sent, raw_response, time_range):
        super(TimeRangeResult, self).__init__(date_time_sent, raw_response)
        self.market_count = time_range.get('marketCount')
        self.time_range = TimeRange(time_range.get('timeRange'))


class Event:

    def __init__(self, event):
        self.id = event.get('id')
        self.open_date = strp_betfair_time(event.get('openDate'))
        self.time_zone = event.get('timezone')
        self.country_code = event.get('countryCode')
        self.name = event.get('name')
        self.venue = event.get('venue')


class EventResult(BetfairModel):

    def __init__(self, date_time_sent, raw_response, event):
        super(EventResult, self).__init__(date_time_sent, raw_response)
        self.market_count = event.get('marketCount')
        self.event = Event(event.get('event'))


class MarketTypeResult(BetfairModel):

    def __init__(self, date_time_sent, raw_response, market_type):
        super(MarketTypeResult, self).__init__(date_time_sent, raw_response)
        self.market_type = market_type.get('marketType')
        self.market_count = market_type.get('marketCount')


class CountryResult(BetfairModel):

    def __init__(self, date_time_sent, raw_response, country):
        super(CountryResult, self).__init__(date_time_sent, raw_response)
        self.country_code = country.get('countryCode')
        self.market_count = country.get('marketCount')


class VenueResult(BetfairModel):

    def __init__(self, date_time_sent, raw_response, venue):
        super(VenueResult, self).__init__(date_time_sent, raw_response)
        self.venue = venue.get('venue')
        self.market_count = venue.get('marketCount')


class MarketCatalogue(BetfairModel):

    def __init__(self, date_time_sent, raw_response, market_catalogue):
        super(MarketCatalogue, self).__init__(date_time_sent, raw_response)
        self.market_id = market_catalogue.get('marketId')
        self.market_name = market_catalogue.get('marketName')
        self.total_matched = market_catalogue.get('totalMatched')
        self.market_start_time = strp_betfair_time(market_catalogue.get('marketStartTime'))
        if 'competition' in market_catalogue:
            self.competition = EventType(market_catalogue.get('competition'))
        if 'event' in market_catalogue:
            self.event = Event(market_catalogue.get('event'))
        if 'eventType' in market_catalogue:
            self.event_type = EventType(market_catalogue.get('eventType'))
        if 'description' in market_catalogue:
            self.description = MarketCatalogueDescription(market_catalogue.get('description'))
        if 'runners' in market_catalogue:
            self.runners = {runner.get('selectionId'): RunnerCatalogue(runner) for runner
                            in market_catalogue.get('runners')}

    @property
    def time_to_start(self):
        return (self.market_start_time-datetime.datetime.now()).total_seconds()


class MarketCatalogueDescription:
    
    def __init__(self, description):
        self.betting_type = description.get('bettingType')
        self.bsp_market = description.get('bspMarket')
        self.discount_allowed = description.get('discountAllowed')
        self.market_base_rate = description.get('marketBaseRate')
        self.market_time = strp_betfair_time(description.get('marketTime'))
        self.market_type = description.get('marketType')
        self.persistence_enabled = description.get('persistenceEnabled')
        self.regulator = description.get('regulator')
        self.rules = description.get('rules')
        self.rules_has_date = description.get('rulesHasDate')
        self.suspend_time = strp_betfair_time(description.get('suspendTime'))
        self.turn_in_play_enabled = description.get('turnInPlayEnabled')
        self.wallet = description.get('wallet')


class RunnerCatalogue:

    def __init__(self, runner_catalogue):
        self.selection_id = runner_catalogue.get('selectionId')
        self.runner_name = runner_catalogue.get('runnerName')
        self.sort_priority = runner_catalogue.get('sortPriority')
        self.handicap = runner_catalogue.get('handicap')
        if 'metadata' in runner_catalogue:
            self.metadata = RunnerCatalogueMetadata(runner_catalogue.get('metadata'))


class RunnerCatalogueMetadata:
    
    def __init__(self, metadata):
        self.runner_id = metadata.get('runnerId')
        self.adjusted_rating = metadata.get('ADJUSTED_RATING')
        self.age = metadata.get('AGE')
        self.bred = metadata.get('BRED')
        self.cloth_number = metadata.get('CLOTH_NUMBER')
        self.cloth_number_alpha = metadata.get('CLOTH_NUMBER_ALPHA')
        self.colours_description = metadata.get('COLOURS_DESCRIPTION')
        self.colours_filename = metadata.get('COLOURS_FILENAME')
        self.colour_type = metadata.get('COLOUR_TYPE')
        self.damsire_bred = metadata.get('DAMSIRE_BRED')
        self.damsire_name = metadata.get('DAMSIRE_NAME')
        self.damsire_year_born = metadata.get('DAMSIRE_YEAR_BORN')
        self.dam_bred = metadata.get('DAM_BRED')
        self.dam_name = metadata.get('DAM_NAME')
        self.dam_year_born = metadata.get('DAM_YEAR_BORN')
        self.days_since_last_run = metadata.get('DAYS_SINCE_LAST_RUN')
        self.forecastprice_denominator = metadata.get('FORECASTPRICE_DENOMINATOR')
        self.forecastprice_numerator = metadata.get('FORECASTPRICE_NUMERATOR')
        self.form = metadata.get('FORM')
        self.jockey_claim = metadata.get('JOCKEY_CLAIM')
        self.jockey_name = metadata.get('JOCKEY_NAME')
        self.official_rating = metadata.get('OFFICIAL_RATING')
        self.owner_name = metadata.get('OWNER_NAME')
        self.sex_type = metadata.get('SEX_TYPE')
        self.sire_bred = metadata.get('SIRE_BRED')
        self.sire_name = metadata.get('SIRE_NAME')
        self.sire_year_born = metadata.get('SIRE_YEAR_BORN')
        self.stall_draw = metadata.get('STALL_DRAW')
        self.trainer_name = metadata.get('TRAINER_NAME')
        self.wearing = metadata.get('WEARING')
        self.weight_units = metadata.get('WEIGHT_UNITS')
        self.weight_value = metadata.get('WEIGHT_VALUE')
        

class MarketBook(BetfairModel):

    def __init__(self, date_time_sent, raw_response, market_book):
        super(MarketBook, self).__init__(date_time_sent, raw_response)
        self.raw_market_book = market_book
        self.market_id = market_book.get('marketId')
        self.bet_delay = market_book.get('betDelay')
        self.bsp_reconciled = market_book.get('bspReconciled')
        self.complete = market_book.get('complete')
        self.cross_matching = market_book.get('crossMatching')
        self.inplay = market_book.get('inplay')
        self.is_market_data_delayed = market_book.get('isMarketDataDelayed')
        self.last_match_time = strp_betfair_time(market_book.get('lastMatchTime'))
        self.number_of_active_runners = market_book.get('numberOfActiveRunners')
        self.number_of_runners = market_book.get('numberOfRunners')
        self.number_of_winners = market_book.get('numberOfWinners')
        self.runners_voidable = market_book.get('runnersVoidable')
        self.status = market_book.get('status')
        self.total_available = market_book.get('totalAvailable')
        self.total_matched = market_book.get('totalMatched')
        self.version = market_book.get('version')
        self.runners = {runner.get('selectionId'): RunnerBook(runner) for runner in market_book.get('runners')}

    @property
    def market_tuple_creator(self):
        csv_tuple = (self.date_time_received, self.market_id,
                     self.cross_matching, self.status, self.inplay, self.total_matched,
                     self.overround, self.underround)
        return csv_tuple

    @property
    def overround(self, over=0.0):
        for runner in self.runners.values():
            if runner.status == 'ACTIVE':
                try:
                    back_a = price_check(runner.ex.available_to_back, 0, 'price')
                    if back_a:
                        over += 1 / back_a
                    else:
                        over += 1
                except AttributeError:
                    return None
        return round(over, 4)

    @property
    def underround(self, under=0.0):
        for runner in self.runners.values():
            if runner.status == 'ACTIVE':
                try:
                    lay_a = price_check(runner.ex.available_to_lay, 0, 'price')
                    if lay_a:
                        under += 1 / lay_a
                except AttributeError:
                    return None
        return round(under, 4)


class RunnerBook:

    def __init__(self, runner_book):
        self.selection_id = runner_book.get('selectionId')
        self.status = runner_book.get('status')
        self.total_matched = runner_book.get('totalMatched')
        self.adjustment_factor = runner_book.get('adjustmentFactor')
        self.handicap = runner_book.get('handicap')
        self.last_price_traded = runner_book.get('lastPriceTraded')
        self.removal_date = strp_betfair_time(runner_book.get('removalDate'))
        if 'sp' in runner_book:
            self.sp = RunnerBookSP(runner_book.get('sp'))
        if 'ex' in runner_book:
            self.ex = RunnerBookEX(runner_book.get('ex'))
        if 'orders' in runner_book:
            self.orders = [RunnerBookOrder(order) for order in runner_book.get('orders')]
        if 'matches' in runner_book:
            self.matches = [RunnerBookMatch(match) for match in runner_book.get('matches')]

    @property
    def runner_tuple_creator_simple(self):
        try:
            back_a = price_check(self.ex.available_to_back, 0, 'price')
            lay_a = price_check(self.ex.available_to_lay, 0, 'price')
        except AttributeError:
            (back_a, lay_a) = (None, None)
        csv_tuple = (self.selection_id, back_a, lay_a, self.last_price_traded, self.total_matched)
        return csv_tuple


class RunnerBookSP:

    def __init__(self, sp):
        self.near_price = sp.get('nearPrice')
        self.far_price = sp.get('farPrice')
        self.back_stake_taken = sp.get('backStakeTaken')
        self.lay_liability_taken = sp.get('layLiabilityTaken')


class RunnerBookEX:

    def __init__(self, ex):
        self.available_to_back = ex.get('availableToBack')
        self.available_to_lay = ex.get('availableToLay')
        self.traded_volume = ex.get('tradedVolume')


class RunnerBookOrder:

    def __init__(self, order):
        self.bet_id = order.get('betId')
        self.avg_price_matched = order.get('avgPriceMatched')
        self.bsp_liability = order.get('bspLiability')
        self.order_type = order.get('orderType')
        self.persistence_type = order.get('persistenceType')
        self.placed_date = strp_betfair_time(order.get('placedDate'))
        self.price = order.get('price')
        self.side = order.get('side')
        self.size = order.get('size')
        self.size_cancelled = order.get('sizeCancelled')
        self.size_lapsed = order.get('sizeLapsed')
        self.size_matched = order.get('sizeMatched')
        self.size_remaining = order.get('sizeRemaining')
        self.size_voided = order.get('sizeVoided')
        self.status = order.get('status')


class RunnerBookMatch:

    def __init__(self, match):
        self.price = match.get('price')
        self.side = match.get('side')
        self.size = match.get('size')


class CurrentOrders(BetfairModel):

    def __init__(self, date_time_sent, raw_response, current_orders):
        super(CurrentOrders, self).__init__(date_time_sent, raw_response)
        self.more_available = current_orders.get('moreAvailable')
        self.orders = [CurrentOrdersOrder(order) for order in current_orders.get('currentOrders')]


class CurrentOrdersOrder:

    def __init__(self, order):
        self.bet_id = order.get('betId')
        self.average_price_matched = order.get('averagePriceMatched')
        self.bsp_liability = order.get('bspLiability')
        self.handicap = order.get('handicap')
        self.market_id = order.get('marketId')
        self.matched_date = strp_betfair_time(order.get('matchedDate'))
        self.order_type = order.get('orderType')
        self.persistence_type = order.get('persistenceType')
        self.placed_date = strp_betfair_time(order.get('placedDate'))
        self.price_size = CurrentOrdersOrderPriceSize(order.get('priceSize'))
        self.regulator_code = order.get('regulatorCode')
        self.selection_id = order.get('selectionId')
        self.side = order.get('side')
        self.size_cancelled = order.get('sizeCancelled')
        self.size_lapsed = order.get('sizeLapsed')
        self.size_matched = order.get('sizeMatched')
        self.size_remaining = order.get('sizeRemaining')
        self.size_voided = order.get('sizeVoided')
        self.status = order.get('status')
        self.bet_id = order.get('betId')


class CurrentOrdersOrderPriceSize:

    def __init__(self, price_size):
        self.price = price_size.get('price')
        self.size = price_size.get('size')


class ClearedOrders(BetfairModel):

    def __init__(self, date_time_sent, raw_response, cleared_orders):
        super(ClearedOrders, self).__init__(date_time_sent, raw_response)
        self.more_available = cleared_orders.get('moreAvailable')
        self.orders = [ClearedOrdersOrder(order) for order in cleared_orders.get('clearedOrders')]


class ClearedOrdersOrder:

    def __init__(self, order):
        self.bet_id = order.get('betId')
        self.bet_count = order.get('betCount')
        self.bet_outcome = order.get('betOutcome')
        self.event_id = order.get('eventId')
        self.event_type_id = order.get('eventTypeId')
        self.handicap = order.get('handicap')
        self.last_matched_date = strp_betfair_time(order.get('lastMatchedDate'))
        self.market_id = order.get('marketId')
        self.order_type = order.get('orderType')
        self.persistence_type = order.get('persistenceType')
        self.placed_date = strp_betfair_time(order.get('placedDate'))
        self.price_matched = order.get('priceMatched')
        self.price_reduced = order.get('priceReduced')
        self.price_requested = order.get('priceRequested')
        self.profit = order.get('profit')
        self.selection_id = order.get('selectionId')
        self.settled_date = strp_betfair_time(order.get('settledDate'))
        self.side = order.get('side')
        self.size_settled = order.get('sizeSettled')


class MarketProfitLoss(BetfairModel):

    def __init__(self, date_time_sent, raw_response, market_profit_loss):
        super(MarketProfitLoss, self).__init__(date_time_sent, raw_response)
        self.market_id = market_profit_loss.get('marketId')
        self.commission_applied = market_profit_loss.get('commissionApplied')
        self.profit_and_losses = [MarketProfitLosses(runner) for runner in market_profit_loss.get('profitAndLosses')]


class MarketProfitLosses:

    def __init__(self, runner):
        self.selection_id = runner.get('selectionId')
        self.if_win = runner.get('ifWin')
        self.if_lose = runner.get('ifLose')
        self.if_place = runner.get('ifPlace')
