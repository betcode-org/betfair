import datetime
import pytest

from fixtures import client
from fixtures import logged_in_client, logged_in_client_aus

from betfairlightweight.apiclient import APIClient
from betfairlightweight.errors.apiexceptions import TransactionCountError, AppKeyError


def test_client_init(client):
    assert client._app_key is None
    assert client.cert == ['/certs/client-2048.crt', '/certs/client-2048.key']
    assert client.transaction_limit == 999
    assert client.exchange == 'UK'
    assert client._session_token is None
    assert client.login_time is None


def test_client_headers(client):
    assert client.login_headers == {'X-Application': 1,
                                    'content-type': 'application/x-www-form-urlencoded'}
    assert client.keep_alive_headers == {'Accept': 'application/json',
                                         'X-Application': client._app_key,
                                         'X-Authentication': client._session_token,
                                         'content-type': 'application/x-www-form-urlencoded'}
    assert client.request_headers == {'X-Application': client._app_key,
                                      'X-Authentication': client._session_token,
                                      'content-type': 'application/json'}


def test_client_app_key(logged_in_client):
    with pytest.raises(AppKeyError):
        logged_in_client.get_app_key()


def test_client_logged_in(logged_in_client):
    assert logged_in_client.login_time is not None
    assert logged_in_client._session_token is not None


def test_client_logged_in_session(logged_in_client):
    assert logged_in_client.session_expired is None
    logged_in_client.login_time = datetime.datetime(2003, 8, 4, 12, 30, 45)
    assert logged_in_client.session_expired is True
    logged_in_client.set_session_token('sessiontoken', 'testcall')
    assert logged_in_client.session_expired is None


def test_client_logged_in_transaction(logged_in_client):
    assert logged_in_client.check_transaction_count(1) is None
    logged_in_client.transaction_count = 1001
    with pytest.raises(TransactionCountError):
        logged_in_client.check_transaction_count(1)


def test_client_logged_in_transaction_reset(logged_in_client):
    logged_in_client.transaction_count = 666
    logged_in_client.next_hour = datetime.datetime(2003, 8, 4, 12, 00, 00)
    logged_in_client.check_transaction_count(1)
    assert logged_in_client.transaction_count == 1


def test_client_logged_in_get_url(logged_in_client, logged_in_client_aus):
    for exchange in ['UK', None]:
        assert logged_in_client.get_url('Login', exchange) == 'https://identitysso.betfair.com/api/certlogin'
        assert logged_in_client.get_url('Logout', exchange) == 'https://identitysso.betfair.com/api/logout'
        assert logged_in_client.get_url('KeepAlive', exchange) == 'https://identitysso.betfair.com/api/keepAlive'
        assert logged_in_client.get_url('BettingRequest', exchange) == 'https://api.betfair.com/exchange/betting/json-rpc/v1'
        assert logged_in_client.get_url('OrderRequest', exchange) == 'https://api.betfair.com/exchange/betting/json-rpc/v1'
        assert logged_in_client.get_url('ScoresRequest', exchange) == 'https://api.betfair.com/exchange/scores/json-rpc/v1'
        assert logged_in_client.get_url('AccountRequest', exchange) == 'https://api.betfair.com/exchange/account/json-rpc/v1'

    for exchange in ['AUS']:
        assert logged_in_client.get_url('Login', exchange) == 'https://identitysso.betfair.com/api/certlogin'
        assert logged_in_client.get_url('Logout', exchange) == 'https://identitysso.betfair.com/api/logout'
        assert logged_in_client.get_url('KeepAlive', exchange) == 'https://identitysso.betfair.com/api/keepAlive'
        assert logged_in_client.get_url('BettingRequest', exchange) == 'https://api-au.betfair.com/exchange/betting/json-rpc/v1'
        assert logged_in_client.get_url('OrderRequest', exchange) == 'https://api-au.betfair.com/exchange/betting/json-rpc/v1'
        assert logged_in_client.get_url('ScoresRequest', exchange) is None
        assert logged_in_client.get_url('AccountRequest', exchange) == 'https://api-au.betfair.com/exchange/account/json-rpc/v1'

    for exchange in ['AUS', None]:
        assert logged_in_client_aus.get_url('Login', exchange) == 'https://identitysso.betfair.com/api/certlogin'
        assert logged_in_client_aus.get_url('Logout', exchange) == 'https://identitysso.betfair.com/api/logout'
        assert logged_in_client_aus.get_url('KeepAlive', exchange) == 'https://identitysso.betfair.com/api/keepAlive'
        assert logged_in_client_aus.get_url('BettingRequest', exchange) == 'https://api-au.betfair.com/exchange/betting/json-rpc/v1'
        assert logged_in_client_aus.get_url('OrderRequest', exchange) == 'https://api-au.betfair.com/exchange/betting/json-rpc/v1'
        assert logged_in_client_aus.get_url('ScoresRequest', exchange) is None
        assert logged_in_client_aus.get_url('AccountRequest', exchange) == 'https://api-au.betfair.com/exchange/account/json-rpc/v1'

    for exchange in ['UK']:
        assert logged_in_client_aus.get_url('Login', exchange) == 'https://identitysso.betfair.com/api/certlogin'
        assert logged_in_client_aus.get_url('Logout', exchange) == 'https://identitysso.betfair.com/api/logout'
        assert logged_in_client_aus.get_url('KeepAlive', exchange) == 'https://identitysso.betfair.com/api/keepAlive'
        assert logged_in_client_aus.get_url('BettingRequest', exchange) == 'https://api.betfair.com/exchange/betting/json-rpc/v1'
        assert logged_in_client_aus.get_url('OrderRequest', exchange) == 'https://api.betfair.com/exchange/betting/json-rpc/v1'
        assert logged_in_client_aus.get_url('ScoresRequest', exchange) == 'https://api.betfair.com/exchange/scores/json-rpc/v1'
        assert logged_in_client_aus.get_url('AccountRequest', exchange) == 'https://api.betfair.com/exchange/account/json-rpc/v1'

    for exchange in ['UK', 'AUS']:
        assert logged_in_client.get_url('NavigationRequest', exchange) == 'https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json'
        assert logged_in_client_aus.get_url('NavigationRequest', exchange) == 'https://api.betfair.com/exchange/betting/rest/v1/en/navigation/menu.json'


def test_client_logged_in_logout(logged_in_client):
    logged_in_client.logout('test')
    assert logged_in_client.login_time is None
    assert logged_in_client._session_token is None
