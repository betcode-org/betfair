import apiparse
from apimethod import Login, KeepAlive, BettingRequest, AccountRequest

def login(api):
    return Login(api).call()


def keep_alive(api):
    return KeepAlive(api).call()


# Betting requests


def list_event_types(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listEventTypes', params).call()


def list_event_types_parsed(api, params):
    response = BettingRequest(api, 'SportsAPING/v1.0/listEventTypes', params).call()
    response_parsed = [apiparse.EventTypes(x) for x in response['result']]
    return response_parsed


def list_competitions(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listCompetitions', params).call()


def list_time_ranges(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listTimeRanges', params).call()


def list_events(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listEvents', params).call()


def list_market_types(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listMarketTypes', params).call()


def list_countries(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listCountries', params).call()


def list_venues(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listVenues', params).call()


def list_market_catalogue(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listMarketCatalogue', params).call()


def list_market_book(api, params):
    return BettingRequest(api, 'SportsAPING/v1.0/listMarketBook', params).call()


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
