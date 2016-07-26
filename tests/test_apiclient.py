import datetime
import unittest
import pytest

from .fixtures import client, client_aus
from .fixtures import logged_in_client, logged_in_client_aus

from betfairlightweight.exceptions import AppKeyError


def test_client_init(client):
    assert client.username == 'username'
    assert client.password == 'password'
    assert client.app_key == 'app_key'
    assert client.exchange == 'UK'
    assert client._login_time is None
    assert client.session_token is None


def test_client_aus_init(client_aus):
    assert client_aus.username == 'username'
    assert client_aus.password == 'password'
    assert client_aus.app_key == 'app_key'
    assert client_aus.exchange == 'AUS'
    assert client_aus._login_time is None
    assert client_aus.session_token is None


def test_client_certs(client):
    # assert client.cert == ['/certs/client-2048.crt', '/certs/client-2048.key']  # fails travis
    pass


def test_set_session_token(client):
    client.set_session_token('test')
    assert client.session_token == 'test'
    assert client._login_time is not None


def test_get_app_key(client):
    client.app_key = None
    with pytest.raises(AppKeyError):
        client.get_app_key()
    client.app_key = 'app_key'


def test_client_headers(logged_in_client):
    assert logged_in_client.login_headers == {'X-Application': 1,
                                              'content-type': 'application/x-www-form-urlencoded'}
    assert logged_in_client.keep_alive_headers == {'Accept': 'application/json',
                                                   'X-Application': logged_in_client.app_key,
                                                   'X-Authentication': logged_in_client.session_token,
                                                   'content-type': 'application/x-www-form-urlencoded'}
    assert logged_in_client.request_headers == {'X-Application': logged_in_client.app_key,
                                                'X-Authentication': logged_in_client.session_token,
                                                'content-type': 'application/json'}


def test_client_logged_in_session(logged_in_client):
    assert logged_in_client.session_expired is None
    logged_in_client._login_time = datetime.datetime(2003, 8, 4, 12, 30, 45)
    assert logged_in_client.session_expired is True
    logged_in_client.set_session_token('sessiontoken')
    assert logged_in_client.session_expired is None


def test_client_logout(logged_in_client):
    logged_in_client.client_logout()
    assert logged_in_client._login_time is None
    assert logged_in_client.session_token is None


# def test_client_logged_in_transaction(logged_in_client):
#     assert logged_in_client.check_transaction_count(1) is None
#     logged_in_client.transaction_count = 1001
#     with pytest.raises(TransactionCountError):
#         logged_in_client.check_transaction_count(1)


# def test_client_logged_in_transaction_reset(logged_in_client):
#     logged_in_client.transaction_count = 666
#     logged_in_client._next_hour = datetime.datetime(2003, 8, 4, 12, 00, 00)
#     logged_in_client.check_transaction_count(1)
#     assert logged_in_client.transaction_count == 1


# def test_client_logged_in_get_url(logged_in_client, logged_in_client_aus):
#     for exchange in ['UK', None]:
#         assert logged_in_client.get_url('Login', exchange) == 'https://identitysso.betfair.com/api/certlogin'
#         assert logged_in_client.get_url('Logout', exchange) == 'https://identitysso.betfair.com/api/logout'
#         assert logged_in_client.get_url('KeepAlive', exchange) == 'https://identitysso.betfair.com/api/keepAlive'
#         assert logged_in_client.get_url('BettingRequest', exchange) == 'https://api.betfair.com/exchange/betting/json-rpc/v1'
#         assert logged_in_client.get_url('OrderRequest', exchange) == 'https://api.betfair.com/exchange/betting/json-rpc/v1'
#         assert logged_in_client.get_url('ScoresRequest', exchange) == 'https://api.betfair.com/exchange/scores/json-rpc/v1'
#         assert logged_in_client.get_url('AccountRequest', exchange) == 'https://api.betfair.com/exchange/account/json-rpc/v1'
#         assert logged_in_client.get_url('ScoresBroadcastRequest', exchange) == 'https://www.betfair.com/inplayservice/v1/scoresAndBroadcast'
#
#     for exchange in ['AUS']:
#         assert logged_in_client.get_url('Login', exchange) == 'https://identitysso.betfair.com/api/certlogin'
#         assert logged_in_client.get_url('Logout', exchange) == 'https://identitysso.betfair.com/api/logout'
#         assert logged_in_client.get_url('KeepAlive', exchange) == 'https://identitysso.betfair.com/api/keepAlive'
#         assert logged_in_client.get_url('BettingRequest', exchange) == 'https://api-au.betfair.com/exchange/betting/json-rpc/v1'
#         assert logged_in_client.get_url('OrderRequest', exchange) == 'https://api-au.betfair.com/exchange/betting/json-rpc/v1'
#         assert logged_in_client.get_url('ScoresRequest', exchange) is None
#         assert logged_in_client.get_url('AccountRequest', exchange) == 'https://api-au.betfair.com/exchange/account/json-rpc/v1'
#
#     for exchange in ['AUS', None]:
#         assert logged_in_client_aus.get_url('Login', exchange) == 'https://identitysso.betfair.com/api/certlogin'
#         assert logged_in_client_aus.get_url('Logout', exchange) == 'https://identitysso.betfair.com/api/logout'
#         assert logged_in_client_aus.get_url('KeepAlive', exchange) == 'https://identitysso.betfair.com/api/keepAlive'
#         assert logged_in_client_aus.get_url('BettingRequest', exchange) == 'https://api-au.betfair.com/exchange/betting/json-rpc/v1'
#         assert logged_in_client_aus.get_url('OrderRequest', exchange) == 'https://api-au.betfair.com/exchange/betting/json-rpc/v1'
#         assert logged_in_client_aus.get_url('ScoresRequest', exchange) is None
#         assert logged_in_client_aus.get_url('AccountRequest', exchange) == 'https://api-au.betfair.com/exchange/account/json-rpc/v1'
#
#     for exchange in ['UK']:
#         assert logged_in_client_aus.get_url('Login', exchange) == 'https://identitysso.betfair.com/api/certlogin'
#         assert logged_in_client_aus.get_url('Logout', exchange) == 'https://identitysso.betfair.com/api/logout'
#         assert logged_in_client_aus.get_url('KeepAlive', exchange) == 'https://identitysso.betfair.com/api/keepAlive'
#         assert logged_in_client_aus.get_url('BettingRequest', exchange) == 'https://api.betfair.com/exchange/betting/json-rpc/v1'
#         assert logged_in_client_aus.get_url('OrderRequest', exchange) == 'https://api.betfair.com/exchange/betting/json-rpc/v1'
#         assert logged_in_client_aus.get_url('ScoresRequest', exchange) == 'https://api.betfair.com/exchange/scores/json-rpc/v1'
#         assert logged_in_client_aus.get_url('AccountRequest', exchange) == 'https://api.betfair.com/exchange/account/json-rpc/v1'
#         assert logged_in_client.get_url('ScoresBroadcastRequest', exchange) == 'https://www.betfair.com/inplayservice/v1/scoresAndBroadcast'
#
#     for exchange in ['UK', 'AUS']:
#         assert logged_in_client.get_url('NavigationRequest', exchange) == 'https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json'
#         assert logged_in_client_aus.get_url('NavigationRequest', exchange) == 'https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json'
