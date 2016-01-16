import logging
from utils import key_check, strp_betfair_time, key_check_datetime


class EventType:

    def __init__(self, event_type):
        self.event_type_id = event_type['eventType']['id']
        self.event_type_name = event_type['eventType']['name']
        self.market_count = event_type['marketCount']


class Competition:

    def __init__(self, competition):
        self.competition_id = competition['competition']['id']
        self.competition_name = competition['competition']['name']
        self.market_count = competition['marketCount']
        self.competition_region = competition['competitionRegion']


class TimeRange:

    def __init__(self, time_range):
        self.market_count = time_range['marketCount']
        self.time_range_from = time_range['timeRange']['from']
        self.time_range_to = time_range['timeRange']['to']


class Event:

    def __init__(self, event):
        self.event_id = event['event']['id']
        self.open_date = strp_betfair_time(event['event']['openDate'])
        self.time_zone = event['event']['timezone']
        self.country_code = key_check(event['event'], 'countryCode')
        self.name = event['event']['name']
        self.market_count = event['marketCount']


class MarketType:

    def __init__(self, market_type):
        self.market_type = market_type['marketType']
        self.market_count = market_type['marketCount']


class Country:

    def __init__(self, country):
        self.country_code = country['countryCode']
        self.market_count = country['marketCount']


class Venue:

    def __init__(self, venue):
        self.venue = venue['venue']
        self.market_count = venue['marketCount']


class MarketCatalogue:

    def __init__(self, market_catalogue):
        self.market_id = market_catalogue['marketId']
        self.market_name = market_catalogue['marketName']
        self.total_matched = market_catalogue['totalMatched']
        self.market_start_time = key_check_datetime(market_catalogue, 'marketStartTime')
        if 'competition' in market_catalogue:
            self.competition = MarketCatalogueCompetition(market_catalogue['competition'])
        if 'event' in market_catalogue:
            self.event = MarketCatalogueEvent(market_catalogue['event'])
        if 'eventType' in market_catalogue:
            self.event_type = MarketCatalogueEventType(market_catalogue['eventType'])
        if 'description' in market_catalogue:
            self.description = MarketCatalogueDescription(market_catalogue['description'])
        if 'runners' in market_catalogue:
            self.runners = []
            for runner in market_catalogue['runners']:
                self.runners.append(RunnerCatalogue(runner))


class MarketCatalogueCompetition:

    def __init__(self, competition):
        self.id = competition['id']
        self.name = ['name']


class MarketCatalogueEvent:

    def __init__(self, event):
        self.id = event['id']
        self.name = event['name']
        self.open_date = strp_betfair_time(event['openDate'])
        self.timezone = event['timezone']


class MarketCatalogueEventType:

    def __init__(self, event_type):
        self.id = event_type['name']
        self.name = event_type['name']


class MarketCatalogueDescription:
    
    def __init__(self, description):
        self.betting_type = description['bettingType']
        self.bsp_market = description['bspMarket']
        self.discount_allowed = description['discountAllowed']
        self.market_base_rate = description['marketBaseRate']
        self.market_time = description['marketTime']
        self.market_type = description['marketType']
        self.persistence_enabled = description['persistenceEnabled']
        self.regulator = description['regulator']
        self.rules = key_check(description, 'rules')
        self.rules_has_date = description['rulesHasDate']
        self.suspend_time = description['suspendTime']
        self.turn_in_play_enabled = description['turnInPlayEnabled']
        self.wallet = description['wallet']


class RunnerCatalogue:

    def __init__(self, runner_catalogue):
        self.selection_id = runner_catalogue['selectionId']
        self.runner_name = runner_catalogue['runnerName']
        self.sort_priority = key_check(runner_catalogue, 'sortPriority')
        self.handicap = runner_catalogue['handicap']
        if 'metadata' in runner_catalogue:
            self.metadata = RunnerCatalogueMetadata(runner_catalogue['metadata'])


class RunnerCatalogueMetadata:
    
    def __init__(self, metadata):
        if len(metadata) == 1:
            self.runner_id = metadata['runnerId']
        elif len(metadata) == 32:
            self.runner_id = metadata['runnerId']
            self.adjusted_rating = metadata['ADJUSTED_RATING']
            self.age = metadata['AGE']
            self.bred = metadata['BRED']
            self.cloth_number = metadata['CLOTH_NUMBER']
            self.cloth_number_alpha = metadata['CLOTH_NUMBER_ALPHA']
            self.colours_description = metadata['COLOURS_DESCRIPTION']
            self.colours_filename = metadata['COLOURS_FILENAME']
            self.colour_type = metadata['COLOUR_TYPE']
            self.damsire_bred = metadata['DAMSIRE_BRED']
            self.damsire_name = metadata['DAMSIRE_NAME']
            self.damsire_year_born = metadata['DAMSIRE_YEAR_BORN']
            self.dam_bred = metadata['DAM_BRED']
            self.dam_name = metadata['DAM_NAME']
            self.dam_year_born = metadata['DAM_YEAR_BORN']
            self.days_since_last_run = metadata['DAYS_SINCE_LAST_RUN']
            self.forecastprice_denominator = metadata['FORECASTPRICE_DENOMINATOR']
            self.forecastprice_numerator = metadata['FORECASTPRICE_NUMERATOR']
            self.form = metadata['FORM']
            self.jockey_claim = metadata['JOCKEY_CLAIM']
            self.jockey_name = metadata['JOCKEY_NAME']
            self.official_rating = metadata['OFFICIAL_RATING']
            self.owner_name = metadata['OWNER_NAME']
            self.sex_type = metadata['SEX_TYPE']
            self.sire_bred = metadata['SIRE_BRED']
            self.sire_name = metadata['SIRE_NAME']
            self.sire_year_born = metadata['SIRE_YEAR_BORN']
            self.stall_draw = metadata['STALL_DRAW']
            self.trainer_name = metadata['TRAINER_NAME']
            self.wearing = metadata['WEARING']
            self.weight_units = metadata['WEIGHT_UNITS']
            self.weight_value = metadata['WEIGHT_VALUE']
        else:
            logging.error('Runner metadata error: %s' % str(metadata['runnerId']))
        

class MarketBook:

    def __init__(self, market_book):
        self.market_id = market_book['marketId']
        self.bet_delay = market_book['betDelay']
        self.bsp_reconciled = market_book['bspReconciled']
        self.complete = market_book['complete']
        self.cross_matching = market_book['crossMatching']
        self.inplay = market_book['inplay']
        self.is_market_data_delayed = market_book['isMarketDataDelayed']
        self.last_match_time = key_check_datetime(market_book, 'lastMatchTime')
        self.number_of_active_runners = market_book['numberOfActiveRunners']
        self.number_of_runners = market_book['numberOfRunners']
        self.number_of_winners = market_book['numberOfWinners']
        self.runners_voidable = market_book['runnersVoidable']
        self.status = market_book['status']
        self.total_available = market_book['totalAvailable']
        self.total_matched = market_book['totalMatched']
        self.version = market_book['version']
        self.runners = []
        for runner in market_book['runners']:
            self.runners.append(RunnerBook(runner))


class RunnerBook:

    def __init__(self, runner_book):
        self.selection_id = runner_book['selectionId']
        self.status = runner_book['status']
        self.total_matched = runner_book['totalMatched']
        self.adjustment_factor = runner_book['adjustmentFactor']
        self.handicap = runner_book['handicap']
        self.last_price_traded = key_check(runner_book, 'lastPriceTraded')
        if 'sp' in runner_book:
            self.sp = RunnerBookSP(runner_book['sp'])
        if 'ex' in runner_book:
            self.ex = RunnerBookEX(runner_book['ex'])
        if 'orders' in runner_book:
            self.orders = runner_book['orders']  # todo
        if 'matched' in runner_book:
            self.matches = runner_book['matches']  # todo


class RunnerBookSP:

    def __init__(self, sp):
        self.near_price = sp['nearPrice']
        self.far_price = sp['farPrice']
        self.back_stake_taken = sp['backStakeTaken']
        self.lay_liability_taken = sp['layLiabilityTaken']


class RunnerBookEX:

    def __init__(self, ex):
        self.available_to_back = ex['availableToBack']
        self.available_to_lay = ex['availableToLay']
        self.traded_volume = ex['tradedVolume']
