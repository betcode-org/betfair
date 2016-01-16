import apiparse
from apimethod import Login, Logout, KeepAlive, BettingRequest, AccountRequest


def login(api):
    return Login(api).call()


def keep_alive(api):
    return KeepAlive(api).call()


def logout(api):
    return Logout(api).call()


# Betting requests todo error handling!


def list_event_types(api, params=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listEventTypes', params).call()
    if parsed:
        return [apiparse.EventType(x) for x in response['result']]
    else:
        return response


def list_competitions(api, params=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listCompetitions', params).call()
    if parsed:
        return [apiparse.Competition(x) for x in response['result']]
    else:
        return response


def list_time_ranges(api, params=None, parsed=True):
    if not params:
        params = {'filter': {},
                  'granularity': 'DAYS'}
    response = BettingRequest(api, 'SportsAPING/v1.0/listTimeRanges', params).call()
    if parsed:
        return [apiparse.TimeRange(x) for x in response['result']]
    else:
        return response


def list_events(api, params=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listEvents', params).call()
    if parsed:
        return [apiparse.Event(x) for x in response['result']]
    else:
        return response


def list_market_types(api, params=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listMarketTypes', params).call()
    if parsed:
        return [apiparse.MarketType(x) for x in response['result']]
    else:
        return response


def list_countries(api, params=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listCountries', params).call()
    if parsed:
        return [apiparse.Country(x) for x in response['result']]
    else:
        return response


def list_venues(api, params=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listVenues', params).call()
    if parsed:
        return [apiparse.Venue(x) for x in response['result']]
    else:
        return response


def list_market_catalogue(api, params=None, parsed=True):
    if not params:
        params = {'filter': {},
                  'maxResults': '1'}
    response = BettingRequest(api, 'SportsAPING/v1.0/listMarketCatalogue', params).call()
    if parsed:
        return [apiparse.MarketCatalogue(x) for x in response['result']]
    else:
        return response


def list_market_book(api, params=None, parsed=True):
    if not params:
        params = {'marketIds': ['1.122618187']}
    response = BettingRequest(api, 'SportsAPING/v1.0/listMarketBook', params).call()
    if parsed:
        return [apiparse.MarketBook(x) for x in response['result']]
    else:
        return response


def place_orders(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/placeOrders', params).call()


def cancel_orders(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/cancelOrders', params).call()


def update_orders(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/updateOrders', params).call()


def replace_orders(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/replaceOrders', params).call()


def list_current_orders(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listCurrentOrders', params).call()


def list_cleared_orders(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listClearedOrders', params).call()


def list_market_profit_and_loss(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listMarketProfitAndLoss', params).call()


# account requests


def get_account_funds(api, params):
    return AccountRequest(api, 'AccountAPING/v1.0/getAccountFunds', params).call()


def get_account_details(api, params):
    return AccountRequest(api, 'AccountAPING/v1.0/getAccountDetails', params).call()


def get_account_statement(api, params):
    return AccountRequest(api, 'AccountAPING/v1.0/getAccountStatement', params).call()


def list_currency_rates(api, params):
    return AccountRequest(api, 'AccountAPING/v1.0/listCurrencyRates', params).call()


def transfer_funds(api, params):
    return AccountRequest(api, 'AccountAPING/v1.0/transferFunds', params).call()
