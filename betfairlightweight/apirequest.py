from apimethod import Login, Logout, KeepAlive, BettingRequest, AccountRequest
from errors.apierrorhandling import api_betting_error_handling, api_login_error_handling, api_keep_alive_error_handling, api_logout_error_handling
from parse import apiparsebetting, apiparseaccount


def login(api):
    response = Login(api).call()
    if not api_login_error_handling(response):
        return
    return response


def keep_alive(api):
    response = KeepAlive(api).call()
    if not api_keep_alive_error_handling(response):
        return
    return response


def logout(api):
    response = Logout(api).call()
    if not api_logout_error_handling(response):
        return
    return response


# Betting requests todo error handling!


def list_event_types(api, params=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listEventTypes', params).call()
    if not api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsebetting.EventType(x) for x in response['result']]
    else:
        return response


def list_competitions(api, params=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listCompetitions', params).call()
    if not api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsebetting.Competition(x) for x in response['result']]
    else:
        return response


def list_time_ranges(api, params=None, parsed=True):
    if not params:
        params = {'filter': {},
                  'granularity': 'DAYS'}
    response = BettingRequest(api, 'SportsAPING/v1.0/listTimeRanges', params).call()
    if not api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsebetting.TimeRange(x) for x in response['result']]
    else:
        return response


def list_events(api, params=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listEvents', params).call()
    if not api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsebetting.Event(x) for x in response['result']]
    else:
        return response


def list_market_types(api, params=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listMarketTypes', params).call()
    if not api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsebetting.MarketType(x) for x in response['result']]
    else:
        return response


def list_countries(api, params=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listCountries', params).call()
    if not api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsebetting.Country(x) for x in response['result']]
    else:
        return response


def list_venues(api, params=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listVenues', params).call()
    if not api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsebetting.Venue(x) for x in response['result']]
    else:
        return response


def list_market_catalogue(api, params=None, parsed=True):
    if not params:
        params = {'filter': {},
                  'maxResults': '1'}
    response = BettingRequest(api, 'SportsAPING/v1.0/listMarketCatalogue', params).call()
    if not api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsebetting.MarketCatalogue(x) for x in response['result']]
    else:
        return response


def list_market_book(api, params=None, parsed=True):
    if not params:
        params = {'marketIds': ['1.122618187']}
    response = BettingRequest(api, 'SportsAPING/v1.0/listMarketBook', params).call()
    if not api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsebetting.MarketBook(x) for x in response['result']]
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


def list_current_orders(api, params=None, parsed=True):  # todo handle moreAvailable
    if not params:
        params = {'dateRange': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listCurrentOrders', params).call()
    if not api_betting_error_handling(response, params):
        return
    if parsed:
        return apiparsebetting.CurrentOrders(response['result'])
    else:
        return response


def list_cleared_orders(api, params=None, parsed=True):  # todo handle moreAvailable & groupby params
    if not params:
        params = {'betStatus': 'SETTLED',
                  'settledDateRange': {},
                  'recordCount': '1000'}
    response = BettingRequest(api, 'SportsAPING/v1.0/listClearedOrders', params).call()
    if not api_betting_error_handling(response, params):
        return
    if parsed:
        return apiparsebetting.ClearedOrders(response['result'])
    else:
        return response


def list_market_profit_and_loss(api, params=None, parsed=True):
    if not params:
        params = {'marketIds': ['1.122617964']}
    response = BettingRequest(api, 'SportsAPING/v1.0/listMarketProfitAndLoss', params).call()
    if not api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsebetting.MarketProfitLoss(x) for x in response['result']]
    else:
        return response


# account requests


def get_account_funds(api, params=None, parsed=True):
    if not params:
        params = {'wallet': 'UK'}  # AUSTRALIAN
    response = AccountRequest(api, 'AccountAPING/v1.0/getAccountFunds', params).call()
    if parsed:
        return apiparseaccount.AccountFunds(response['result'])
    else:
        return response


def get_account_details(api, params=None, parsed=True):
    if not params:
        params = {}
    response = AccountRequest(api, 'AccountAPING/v1.0/getAccountDetails', params).call()
    if parsed:
        return apiparseaccount.AccountDetails(response['result'])
    else:
        return response


def get_account_statement(api, params=None, parsed=True):
    if not params:
        params = {'itemDateRange': {},
                  'includeItem': 'ALL'}
    response = AccountRequest(api, 'AccountAPING/v1.0/getAccountStatement', params).call()
    if parsed:
        return apiparseaccount.AccountStatement(response['result'])
    else:
        return response


def list_currency_rates(api, params=None, parsed=True):
    if not params:
        params = {'fromCurrency': 'GBP'}
    response = AccountRequest(api, 'AccountAPING/v1.0/listCurrencyRates', params).call()
    if parsed:
        return [apiparseaccount.CurrencyRate(x) for x in response['result']]
    else:
        return response


def transfer_funds(api, params=None, parsed=True):
    if not params:
        params = {'from': 'UK',
                  'to': 'AUSTRALIAN',
                  'amount': '0.01'}
    response = AccountRequest(api, 'AccountAPING/v1.0/transferFunds', params).call()
    if parsed:
        return apiparseaccount.TransferFunds(response['result'])
    else:
        return response
