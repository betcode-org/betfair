from .parse import apiparsedata, apiparseaccount, apiparsebetting, apiparsescores
from .apimethod import (
    Login, Logout, KeepAlive, BettingRequest, AccountRequest, ScoresRequest, OrderRequest, NavigationRequest)
from .utils import process_response, api_request


"""
Below lists all api requests
"""


def login(api):
    request = Login(api)
    (response, raw_response, sent) = request()
    api.set_session_token(response.get('sessionToken'), 'Login')
    return response


def keep_alive(api):
    request = KeepAlive(api)
    (response, raw_response, sent) = request()
    api.set_session_token(response.get('token'), 'KeepAlive')
    return response


def logout(api):
    request = Logout(api)
    (response, raw_response, sent) = request()
    api.logout(response.get('status'))
    return response


# Betting requests
# todo add decorator to check logged in / keep alive status?


@api_request
def list_event_types(api, params=None, session=None, exchange=None):
    request = BettingRequest(api, 'SportsAPING/v1.0/listEventTypes', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparsedata.EventTypeResult)


@api_request
def list_competitions(api, params=None, session=None, exchange=None):
    request = BettingRequest(api, 'SportsAPING/v1.0/listCompetitions', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparsedata.CompetitionResult)


@api_request
def list_time_ranges(api, params=None, session=None, exchange=None):
    request = BettingRequest(api, 'SportsAPING/v1.0/listTimeRanges', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparsedata.TimeRangeResult)


@api_request
def list_events(api, params=None, session=None, exchange=None):
    request = BettingRequest(api, 'SportsAPING/v1.0/listEvents', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparsedata.EventResult)


@api_request
def list_market_types(api, params=None, session=None, exchange=None):
    request = BettingRequest(api, 'SportsAPING/v1.0/listMarketTypes', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparsedata.MarketTypeResult)


@api_request
def list_countries(api, params=None, session=None, exchange=None):
    request = BettingRequest(api, 'SportsAPING/v1.0/listCountries', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparsedata.CountryResult)


@api_request
def list_venues(api, params=None, session=None, exchange=None):
    request = BettingRequest(api, 'SportsAPING/v1.0/listVenues', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparsedata.VenueResult)


@api_request
def list_market_catalogue(api, params=None, session=None, exchange=None):
    request = BettingRequest(api, 'SportsAPING/v1.0/listMarketCatalogue', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparsedata.MarketCatalogue)


@api_request
def list_market_book(api, params=None, session=None, exchange=None):
    request = BettingRequest(api, 'SportsAPING/v1.0/listMarketBook', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparsedata.MarketBook)


# order requests

@api_request
def place_orders(api, params=None, session=None, exchange=None):  # atomic
    request = OrderRequest(api, 'SportsAPING/v1.0/placeOrders', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparsebetting.PlaceOrder)


@api_request
def cancel_orders(api, params=None, session=None, exchange=None):
    request = OrderRequest(api, 'SportsAPING/v1.0/cancelOrders', params, exchange)
    (response, raw_response, sent) = request(session)
    if params:
        return process_response(response, raw_response, sent, apiparsebetting.CancelOrder)
    else:
        return process_response(response, raw_response, sent, apiparsebetting.CancelAllOrders)


@api_request
def update_orders(api, params=None, session=None, exchange=None):
    request = OrderRequest(api, 'SportsAPING/v1.0/updateOrders', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparsebetting.UpdateOrder)


@api_request
def replace_orders(api, params=None, session=None, exchange=None):
    request = OrderRequest(api, 'SportsAPING/v1.0/replaceOrders', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparsebetting.ReplaceOrder)


@api_request
def list_current_orders(api, params=None, session=None, exchange=None):
    request = BettingRequest(api, 'SportsAPING/v1.0/listCurrentOrders', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparsedata.CurrentOrders)


@api_request
def list_cleared_orders(api, params=None, session=None, exchange=None):
    request = BettingRequest(api, 'SportsAPING/v1.0/listClearedOrders', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparsedata.ClearedOrders)


@api_request
def list_market_profit_and_loss(api, params=None, session=None, exchange=None):
    request = BettingRequest(api, 'SportsAPING/v1.0/listMarketProfitAndLoss', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparsedata.MarketProfitLoss)


@api_request
def list_race_status(api, params=None, session=None, exchange=None):
    request = ScoresRequest(api, 'ScoresAPING/v1.0/listRaceDetails', params)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparsescores.RaceStatus)


# account requests  # todo account error handling

@api_request
def get_account_funds(api, params=None, session=None, exchange=None):
    request = AccountRequest(api, 'AccountAPING/v1.0/getAccountFunds', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparseaccount.AccountFunds)


@api_request
def get_account_details(api, params=None, session=None, exchange=None):
    request = AccountRequest(api, 'AccountAPING/v1.0/getAccountDetails', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparseaccount.AccountDetails)


@api_request
def get_account_statement(api, params=None, session=None, exchange=None):
    request = AccountRequest(api, 'AccountAPING/v1.0/getAccountStatement', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparseaccount.AccountStatement)


@api_request
def list_currency_rates(api, params=None, session=None, exchange=None):
    request = AccountRequest(api, 'AccountAPING/v1.0/listCurrencyRates', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparseaccount.CurrencyRate)


@api_request
def transfer_funds(api, params=None, session=None, exchange=None):
    request = AccountRequest(api, 'AccountAPING/v1.0/transferFunds', params, exchange)
    (response, raw_response, sent) = request(session)
    return process_response(response, raw_response, sent, apiparseaccount.TransferFunds)


# navigation requests

def list_navigation(api, params='UK'):
    request = NavigationRequest(api, params)
    (response, raw_response, sent) = request()
    return response
