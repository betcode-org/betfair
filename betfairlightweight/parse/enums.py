from enum import Enum


class MockParams(Enum):
    list_event_types = {'filter': {}}
    list_competitions = {'filter': {}}
    list_time_ranges = {'filter': {},
                        'granularity': 'DAYS'}
    list_events = {'filter': {}}
    list_market_types = {'filter': {}}
    list_countries = {'filter': {}}
    list_venues = {'filter': {}}
    list_market_catalogue = {'filter': {},
                             'maxResults': '1'}
    list_market_book = {'marketIds': ['1.122618187']}
    place_orders = {}
    cancel_orders = {}
    update_orders = {}
    replace_orders = {}
    list_current_orders = {'dateRange': {}}
    list_cleared_orders = {'betStatus': 'SETTLED',
                           'settledDateRange': {},
                           'recordCount': '1000'}
    list_market_profit_and_loss = {'marketIds': ['1.122617964']}
    list_race_status = {}
    get_account_funds = {'wallet': None}
    get_account_details = {}
    get_account_statement = {'itemDateRange': {},
                             'includeItem': 'ALL'}
    list_currency_rates = {'fromCurrency': 'GBP'}
    transfer_funds = {'from': 'UK',
                      'to': 'AUSTRALIAN',
                      'amount': '0.00'}


class RaceStatusEnum(Enum):
    DORMANT = 'There is no data available for this race.'
    DELAYED = 'The start of the race has been delayed'
    PARADING = 'The horses are in the parade ring'
    GOINGDOWN = 'The horses are going down to the starting post'
    GOINGBEHIND = 'The horses are going behind the stalls'
    ATTHEPOST = 'The horses are at the post'
    UNDERORDERS = 'The horses are loaded into the stalls/race is about to start'
    OFF = 'The race has started'
    FINISHED = 'The race has finished'
    FALSESTART = 'There has been a false start'
    PHOTOGRAPH = 'The result of the race is subject to a photo finish'
    RESULT = 'The result of the race has been announced'
    WEIGHEDIN = 'The jockeys have weighed in'
    RACEVOID = 'The race has been declared void'
    ABANDONED = 'The meeting has been cancelled'
