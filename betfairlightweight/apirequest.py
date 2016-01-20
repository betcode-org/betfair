import datetime
from errors import apierrorhandling
from parse import apiparsedata, apiparseaccount, apiparsebetting
from apimethod import Login, Logout, KeepAlive, BettingRequest, AccountRequest


def login(api):
    response = Login(api).call()
    if not apierrorhandling.api_login_error_handling(response):
        return
    return response


def keep_alive(api):
    response = KeepAlive(api).call()
    if not apierrorhandling.api_keep_alive_error_handling(response):
        return
    return response


def logout(api):
    response = Logout(api).call()
    if not apierrorhandling.api_logout_error_handling(response):
        return
    return response


# Betting requests todo params error handling! / move date_time_created to apirequest


def list_event_types(api, params=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listEventTypes', params).call()
    if not apierrorhandling.api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsedata.EventType(x) for x in response['result']]
    else:
        return response


def list_competitions(api, params=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listCompetitions', params).call()
    if not apierrorhandling.api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsedata.Competition(x) for x in response['result']]
    else:
        return response


def list_time_ranges(api, params=None, parsed=True):
    if not params:
        params = {'filter': {},
                  'granularity': 'DAYS'}
    response = BettingRequest(api, 'SportsAPING/v1.0/listTimeRanges', params).call()
    if not apierrorhandling.api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsedata.TimeRange(x) for x in response['result']]
    else:
        return response


def list_events(api, params=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listEvents', params).call()
    if not apierrorhandling.api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsedata.Event(x) for x in response['result']]
    else:
        return response


def list_market_types(api, params=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listMarketTypes', params).call()
    if not apierrorhandling.api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsedata.MarketType(x) for x in response['result']]
    else:
        return response


def list_countries(api, params=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listCountries', params).call()
    if not apierrorhandling.api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsedata.Country(x) for x in response['result']]
    else:
        return response


def list_venues(api, params=None, parsed=True):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listVenues', params).call()
    if not apierrorhandling.api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsedata.Venue(x) for x in response['result']]
    else:
        return response


def list_market_catalogue(api, params=None, parsed=True):
    if not params:
        params = {'filter': {},
                  'maxResults': '1'}
    response = BettingRequest(api, 'SportsAPING/v1.0/listMarketCatalogue', params).call()
    if not apierrorhandling.api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsedata.MarketCatalogue(x) for x in response['result']]
    else:
        return response


def list_market_book(api, params=None, parsed=True):
    if not params:
        params = {'marketIds': ['1.122618187']}
    response = BettingRequest(api, 'SportsAPING/v1.0/listMarketBook', params).call()
    if not apierrorhandling.api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsedata.MarketBook(x) for x in response['result']]
    else:
        return response

# order requests


def place_orders(api, params, parsed=True):  # atomic
    response = BettingRequest(api, 'SportsAPING/v1.0/placeOrders', params).call()
    date_time_received = datetime.datetime.now()
    apierrorhandling.api_order_error_handling(response)
    if 'error' in response:
        return
    if parsed:
        return apiparsebetting.PlaceOrder(response['result'], date_time_received)
    else:
        return response


def cancel_orders(api, params=None, parsed=True):
    if not params:
        params = {}  # cancel ALL orders
    response = BettingRequest(api, 'SportsAPING/v1.0/cancelOrders', params).call()
    date_time_received = datetime.datetime.now()
    apierrorhandling.api_order_error_handling(response)
    if 'error' in response:
        return
    if parsed:
        return apiparsebetting.CancelOrder(response['result'], date_time_received)
    else:
        return response


def update_orders(api, params, parsed=True):
    response = BettingRequest(api, 'SportsAPING/v1.0/updateOrders', params).call()
    date_time_received = datetime.datetime.now()
    apierrorhandling.api_order_error_handling(response)
    if 'error' in response:
        return
    if parsed:
        return apiparsebetting.UpdateOrder(response['result'], date_time_received)
    else:
        return response


def replace_orders(api, params, parsed=True):
    response = BettingRequest(api, 'SportsAPING/v1.0/replaceOrders', params).call()
    date_time_received = datetime.datetime.now()
    apierrorhandling.api_order_error_handling(response)
    if 'error' in response:
        return
    if parsed:
        return apiparsebetting.ReplaceOrder(response['result'], date_time_received)
    else:
        return response


def list_current_orders(api, params=None, parsed=True):  # todo handle moreAvailable
    if not params:
        params = {'dateRange': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listCurrentOrders', params).call()
    if not apierrorhandling.api_betting_error_handling(response, params):
        return
    if parsed:
        return apiparsedata.CurrentOrders(response['result'])
    else:
        return response


def list_cleared_orders(api, params=None, parsed=True):  # todo handle moreAvailable & groupby params
    if not params:
        params = {'betStatus': 'SETTLED',
                  'settledDateRange': {},
                  'recordCount': '1000'}
    response = BettingRequest(api, 'SportsAPING/v1.0/listClearedOrders', params).call()
    if not apierrorhandling.api_betting_error_handling(response, params):
        return
    if parsed:
        return apiparsedata.ClearedOrders(response['result'])
    else:
        return response


def list_market_profit_and_loss(api, params=None, parsed=True):
    if not params:
        params = {'marketIds': ['1.122617964']}
    response = BettingRequest(api, 'SportsAPING/v1.0/listMarketProfitAndLoss', params).call()
    if not apierrorhandling.api_betting_error_handling(response, params):
        return
    if parsed:
        return [apiparsedata.MarketProfitLoss(x) for x in response['result']]
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
