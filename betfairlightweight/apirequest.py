import datetime
from betfairlightweight.errors.apiexceptions import APIError, LoginError, KeepAliveError, LogoutError
from betfairlightweight.errors import apierrorhandling
from betfairlightweight.parse import apiparsedata, apiparseaccount, apiparsebetting, apiparsescores
from betfairlightweight.apimethod import Login, Logout, KeepAlive, BettingRequest, AccountRequest, ScoresRequest
from betfairlightweight.apimethod import NavigationRequest


def login(api):
    response = Login(api).call()
    apierrorhandling.api_login_error_handling(response)
    return response


def keep_alive(api):
    response = KeepAlive(api).call()
    apierrorhandling.api_keep_alive_error_handling(response)
    return response


def logout(api):
    response = Logout(api).call()
    apierrorhandling.api_logout_error_handling(response)
    return response


# Betting requests todo add decorator to check logged in / keep alive status?


def list_event_types(api, params=None, session=None, parsed=True, exchange=None):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listEventTypes', params, exchange).call(session)
    (response, raw_response, sent) = response
    apierrorhandling.api_betting_error_handling(response, params)
    if parsed:
        return [apiparsedata.EventType(sent, raw_response, x) for x in response['result']]
    else:
        return response


def list_competitions(api, params=None, session=None, parsed=True, exchange=None):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listCompetitions', params, exchange).call(session)
    (response, raw_response, sent) = response
    apierrorhandling.api_betting_error_handling(response, params)
    if parsed:
        return [apiparsedata.Competition(sent, raw_response, x) for x in response['result']]
    else:
        return response


def list_time_ranges(api, params=None, session=None, parsed=True, exchange=None):
    if not params:
        params = {'filter': {},
                  'granularity': 'DAYS'}
    response = BettingRequest(api, 'SportsAPING/v1.0/listTimeRanges', params, exchange).call(session)
    (response, raw_response, sent) = response
    apierrorhandling.api_betting_error_handling(response, params)
    if parsed:
        return [apiparsedata.TimeRange(sent, raw_response, x) for x in response['result']]
    else:
        return response


def list_events(api, params=None, session=None, parsed=True, exchange=None):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listEvents', params, exchange).call(session)
    (response, raw_response, sent) = response
    apierrorhandling.api_betting_error_handling(response, params)
    if parsed:
        return [apiparsedata.Event(sent, raw_response, x) for x in response['result']]
    else:
        return response


def list_market_types(api, params=None, session=None, parsed=True, exchange=None):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listMarketTypes', params, exchange).call(session)
    (response, raw_response, sent) = response
    apierrorhandling.api_betting_error_handling(response, params)
    if parsed:
        return [apiparsedata.MarketType(sent, raw_response, x) for x in response['result']]
    else:
        return response


def list_countries(api, params=None, session=None, parsed=True, exchange=None):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listCountries', params, exchange).call(session)
    (response, raw_response, sent) = response
    apierrorhandling.api_betting_error_handling(response, params)
    if parsed:
        return [apiparsedata.Country(sent, raw_response, x) for x in response['result']]
    else:
        return response


def list_venues(api, params=None, session=None, parsed=True, exchange=None):
    if not params:
        params = {'filter': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listVenues', params, exchange).call(session)
    (response, raw_response, sent) = response
    apierrorhandling.api_betting_error_handling(response, params)
    if parsed:
        return [apiparsedata.Venue(sent, raw_response, x) for x in response['result']]
    else:
        return response


def list_market_catalogue(api, params=None, session=None, parsed=True, exchange=None):
    if not params:
        params = {'filter': {},
                  'maxResults': '1'}
    response = BettingRequest(api, 'SportsAPING/v1.0/listMarketCatalogue', params, exchange).call(session)
    (response, raw_response, sent) = response
    apierrorhandling.api_betting_error_handling(response, params)
    if parsed:
        return [apiparsedata.MarketCatalogue(sent, raw_response, x) for x in response['result']]
    else:
        return response


def list_market_book(api, params=None, session=None, parsed=True, exchange=None):
    if not params:
        params = {'marketIds': ['1.122618187']}
    response = BettingRequest(api, 'SportsAPING/v1.0/listMarketBook', params, exchange).call(session)
    (response, raw_response, sent) = response
    apierrorhandling.api_betting_error_handling(response, params)
    if parsed:
        return [apiparsedata.MarketBook(sent, raw_response, x) for x in response['result']]
    else:
        return response

# order requests


def place_orders(api, params, session=None, parsed=True, exchange=None):  # atomic
    response = BettingRequest(api, 'SportsAPING/v1.0/placeOrders', params, exchange).call(session)
    (response, raw_response, sent) = response
    date_time_received = datetime.datetime.now()
    apierrorhandling.api_order_error_handling(response, params, 'SportsAPING/v1.0/placeOrders')
    if parsed:
        return apiparsebetting.PlaceOrder(sent, raw_response, response['result'], date_time_received)
    else:
        return response


def cancel_orders(api, params=None, session=None, parsed=True, exchange=None):
    if not params:
        params = {}  # cancel ALL orders
    response = BettingRequest(api, 'SportsAPING/v1.0/cancelOrders', params, exchange).call(session)
    (response, raw_response, sent) = response
    date_time_received = datetime.datetime.now()
    apierrorhandling.api_order_error_handling(response, params, 'SportsAPING/v1.0/cancelOrders')
    if parsed:
        if params:
            return apiparsebetting.CancelOrder(sent, raw_response, response['result'], date_time_received)
        else:
            return apiparsebetting.CancelAllOrders(sent, raw_response, response['result'], date_time_received)
    else:
        return response


def update_orders(api, params, session=None, parsed=True, exchange=None):
    response = BettingRequest(api, 'SportsAPING/v1.0/updateOrders', params, exchange).call(session)
    (response, raw_response, sent) = response
    date_time_received = datetime.datetime.now()
    apierrorhandling.api_order_error_handling(response, params, 'SportsAPING/v1.0/updateOrders')
    if parsed:
        return apiparsebetting.UpdateOrder(sent, raw_response, response['result'], date_time_received)
    else:
        return response


def replace_orders(api, params, session=None, parsed=True, exchange=None):
    response = BettingRequest(api, 'SportsAPING/v1.0/replaceOrders', params, exchange).call(session)
    (response, raw_response, sent) = response
    date_time_received = datetime.datetime.now()
    apierrorhandling.api_order_error_handling(response, params, 'SportsAPING/v1.0/replaceOrders')
    if parsed:
        return apiparsebetting.ReplaceOrder(sent, raw_response, response['result'], date_time_received)
    else:
        return response


def list_current_orders(api, params=None, session=None, parsed=True, exchange=None):
    if not params:
        params = {'dateRange': {}}
    response = BettingRequest(api, 'SportsAPING/v1.0/listCurrentOrders', params, exchange).call(session)
    (response, raw_response, sent) = response
    apierrorhandling.api_betting_error_handling(response, params)
    if parsed:
        return apiparsedata.CurrentOrders(sent, raw_response, response['result'])
    else:
        return response


def list_cleared_orders(api, params=None, session=None, parsed=True, exchange=None):
    if not params:
        params = {'betStatus': 'SETTLED',
                  'settledDateRange': {},
                  'recordCount': '1000'}
    response = BettingRequest(api, 'SportsAPING/v1.0/listClearedOrders', params, exchange).call(session)
    (response, raw_response, sent) = response
    apierrorhandling.api_betting_error_handling(response, params)
    if parsed:
        return apiparsedata.ClearedOrders(sent, raw_response, response['result'])
    else:
        return response


def list_market_profit_and_loss(api, params=None, session=None, parsed=True, exchange=None):
    if not params:
        params = {'marketIds': ['1.122617964']}
    response = BettingRequest(api, 'SportsAPING/v1.0/listMarketProfitAndLoss', params, exchange).call(session)
    (response, raw_response, sent) = response
    apierrorhandling.api_betting_error_handling(response, params)
    if parsed:
        return [apiparsedata.MarketProfitLoss(sent, raw_response, x) for x in response['result']]
    else:
        return response


def list_race_status(api, params, session=None, parsed=True):
    response = ScoresRequest(api, 'ScoresAPING/v1.0/listRaceDetails', params).call(session)
    (response, raw_response, sent) = response
    apierrorhandling.api_betting_error_handling(response, params)
    if parsed:
        return [apiparsescores.RaceStatus(sent, raw_response, x) for x in response['result']]
    else:
        return response


# account requests  # todo account error handling


def get_account_funds(api, params=None, session=None, parsed=True, exchange=None):
    if not params:
        params = {'wallet': None}  # AUSTRALIAN
    response = AccountRequest(api, 'AccountAPING/v1.0/getAccountFunds', params, exchange).call(session)
    (response, raw_response, sent) = response
    if parsed:
        return apiparseaccount.AccountFunds(sent, raw_response, response['result'])
    else:
        return response


def get_account_details(api, params=None, session=None, parsed=True, exchange=None):
    if not params:
        params = {}
    response = AccountRequest(api, 'AccountAPING/v1.0/getAccountDetails', params, exchange).call(session)
    (response, raw_response, sent) = response
    if parsed:
        return apiparseaccount.AccountDetails(sent, raw_response, response['result'])
    else:
        return response


def get_account_statement(api, params=None, session=None, parsed=True, exchange=None):
    if not params:
        params = {'itemDateRange': {},
                  'includeItem': 'ALL'}
    response = AccountRequest(api, 'AccountAPING/v1.0/getAccountStatement', params, exchange).call(session)
    (response, raw_response, sent) = response
    if parsed:
        return apiparseaccount.AccountStatement(sent, raw_response, response['result'])
    else:
        return response


def list_currency_rates(api, params=None, session=None, parsed=True, exchange=None):
    if not params:
        params = {'fromCurrency': 'GBP'}
    response = AccountRequest(api, 'AccountAPING/v1.0/listCurrencyRates', params, exchange).call(session)
    (response, raw_response, sent) = response
    if parsed:
        return [apiparseaccount.CurrencyRate(sent, raw_response, x) for x in response['result']]
    else:
        return response


def transfer_funds(api, params=None, session=None, parsed=True, exchange=None):
    if not params:
        params = {'from': None,
                  'to': 'AUSTRALIAN',
                  'amount': '0.00'}
    response = AccountRequest(api, 'AccountAPING/v1.0/transferFunds', params, exchange).call(session)
    (response, raw_response, sent) = response
    if parsed:
        return apiparseaccount.TransferFunds(sent, raw_response, response['result'])
    else:
        return response

# navigation requests


def list_navigation(api, params='UK'):
    response = NavigationRequest(api, params).call()
    (response, raw_response, sent) = response
    return response
