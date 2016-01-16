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
            self.competition_id = market_catalogue['competition']['id']
            self.competition_name = market_catalogue['competition']['name']
        if 'event' in market_catalogue:
            self.event_id = market_catalogue['event']['id']
            self.event_name = market_catalogue['event']['name']
            self.event_open_date = strp_betfair_time(market_catalogue['event']['openDate'])
            self.event_timezone = market_catalogue['event']['timezone']
        if 'eventType' in market_catalogue:
            self.event_type_id = market_catalogue['eventType']['name']
            self.event_type_name = market_catalogue['eventType']['name']
        if 'description' in market_catalogue:
            self.description_betting_type = market_catalogue['description']['bettingType']
            self.description_bsp_market = market_catalogue['description']['bspMarket']
            self.description_discount_allowed = market_catalogue['description']['discountAllowed']
            self.description_market_base_rate = market_catalogue['description']['marketBaseRate']
            self.description_market_time = market_catalogue['description']['marketTime']
            self.description_market_type = market_catalogue['description']['marketType']
            self.description_persistence_enabled = market_catalogue['description']['persistenceEnabled']
            self.description_regulator = market_catalogue['description']['regulator']
            self.description_rules = key_check(market_catalogue['description'], 'rules')
            self.description_rules_has_date = market_catalogue['description']['rulesHasDate']
            self.description_suspend_time = market_catalogue['description']['suspendTime']
            self.description_turn_in_play_enabled = market_catalogue['description']['turnInPlayEnabled']
            self.description_wallet = market_catalogue['description']['wallet']
        if 'runners' in market_catalogue:
            self.runners = []
            for runner in market_catalogue['runners']:
                self.runners.append(RunnerCatalogue(runner))


class RunnerCatalogue:

    def __init__(self, runner_catalogue):
        self.selection_id = runner_catalogue['selectionId']
        self.runner_name = runner_catalogue['runnerName']
        self.sort_priority = key_check(runner_catalogue, 'sortPriority')
        self.handicap = runner_catalogue['handicap']
        if 'metadata' in runner_catalogue:
            self.metadata_runner_id = runner_catalogue['metadata']['runnerId']
            if len(runner_catalogue['metadata']) == 1:
                return
            elif len(runner_catalogue['metadata']) == 32:
                self.metadata_adjusted_rating = runner_catalogue['metadata']['ADJUSTED_RATING']
                self.metadata_age = runner_catalogue['metadata']['AGE']
                self.metadata_bred = runner_catalogue['metadata']['BRED']
                self.metadata_cloth_number = runner_catalogue['metadata']['CLOTH_NUMBER']
                self.metadata_cloth_number_alpha = runner_catalogue['metadata']['CLOTH_NUMBER_ALPHA']
                self.metadata_colours_description = runner_catalogue['metadata']['COLOURS_DESCRIPTION']
                self.metadata_colours_filename = runner_catalogue['metadata']['COLOURS_FILENAME']
                self.metadata_colour_type = runner_catalogue['metadata']['COLOUR_TYPE']
                self.metadata_damsire_bred = runner_catalogue['metadata']['DAMSIRE_BRED']
                self.metadata_damsire_name = runner_catalogue['metadata']['DAMSIRE_NAME']
                self.metadata_damsire_year_born = runner_catalogue['metadata']['DAMSIRE_YEAR_BORN']
                self.metadata_dam_bred = runner_catalogue['metadata']['DAM_BRED']
                self.metadata_dam_name = runner_catalogue['metadata']['DAM_NAME']
                self.metadata_dam_year_born = runner_catalogue['metadata']['DAM_YEAR_BORN']
                self.metadata_days_since_last_run = runner_catalogue['metadata']['DAYS_SINCE_LAST_RUN']
                self.metadata_forecastprice_denominator = runner_catalogue['metadata']['FORECASTPRICE_DENOMINATOR']
                self.metadata_forecastprice_numerator = runner_catalogue['metadata']['FORECASTPRICE_NUMERATOR']
                self.metadata_form = runner_catalogue['metadata']['FORM']
                self.metadata_jockey_claim = runner_catalogue['metadata']['JOCKEY_CLAIM']
                self.metadata_jockey_name = runner_catalogue['metadata']['JOCKEY_NAME']
                self.metadata_official_rating = runner_catalogue['metadata']['OFFICIAL_RATING']
                self.metadata_owner_name = runner_catalogue['metadata']['OWNER_NAME']
                self.metadata_sex_type = runner_catalogue['metadata']['SEX_TYPE']
                self.metadata_sire_bred = runner_catalogue['metadata']['SIRE_BRED']
                self.metadata_sire_name = runner_catalogue['metadata']['SIRE_NAME']
                self.metadata_sire_year_born = runner_catalogue['metadata']['SIRE_YEAR_BORN']
                self.metadata_stall_draw = runner_catalogue['metadata']['STALL_DRAW']
                self.metadata_trainer_name = runner_catalogue['metadata']['TRAINER_NAME']
                self.metadata_wearing = runner_catalogue['metadata']['WEARING']
                self.metadata_weight_units = runner_catalogue['metadata']['WEIGHT_UNITS']
                self.metadata_weight_value = runner_catalogue['metadata']['WEIGHT_VALUE']
            else:
                logging.error('Runner metadata error: %s' % str(runner_catalogue['selectionId']))


class MarketBook:

    def __init__(self, market_book):
        self.market_id = market_book['marketId']
        self.bet_delay = market_book['betDelay']
        self.bsp_reconciled = market_book['bspReconciled']
        self.complete = market_book['complete']
        self.corss_matching = market_book['crossMatching']
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
            self.sp_near_price = runner_book['sp']['nearPrice']
            self.sp_far_price = runner_book['sp']['farPrice']
            self.sp_back_stake_taken = runner_book['sp']['backStakeTaken']
            self.sp_lay_liability_taken = runner_book['sp']['layLiabilityTaken']
        if 'ex' in runner_book:
            self.ex_available_to_back = runner_book['ex']['availableToBack']
            self.ex_available_to_lay = runner_book['ex']['availableToLay']
            self.ex_traded_volume = runner_book['ex']['tradedVolume']
        if 'orders' in runner_book:
            self.orders = runner_book['orders']  # todo
        if 'matched' in runner_book:
            self.matches = runner_book['matches']  # todo
