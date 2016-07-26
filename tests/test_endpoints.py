import json
import pytest

from .fixtures import client, logged_in_client, logged_in_client_aus, client_base_endpoint

from betfairlightweight.exceptions import APIError, LoginError, LogoutError, KeepAliveError


def test_base_endpoint_init(client_base_endpoint, logged_in_client):
    assert client_base_endpoint.timeout == 3.05
    assert client_base_endpoint._error == APIError
    assert client_base_endpoint.exchange == logged_in_client.exchange


def test_base_endpoint_req(client_base_endpoint):
    payload = {'jsonrpc': '2.0',
               'method': 'test',
               'params': 'empty',
               'id': 1}
    assert client_base_endpoint.create_req('test', 'empty') == json.dumps(payload)


def test_base_endpoint_create_resp(client_base_endpoint):
    pass


def test_base_endpoint_error_handler(client_base_endpoint):
    response = {'result': 'empty'}
    assert client_base_endpoint._error_handler(response) is None

    response = {'error': {'code': -32700}}
    with pytest.raises(APIError):
        client_base_endpoint._error_handler(response)


def test_login_endpoint_init(logged_in_client):
    assert logged_in_client.login.timeout == 3.05
    assert logged_in_client.login._error == LoginError
    assert logged_in_client.login._endpoints_uk.get('Login') == 'https://identitysso.betfair.com/api/certlogin'


def test_login_error_handler(logged_in_client):
    assert logged_in_client.login._error_handler({'loginStatus': 'SUCCESS'}) is None
    with pytest.raises(LoginError):
        logged_in_client.login._error_handler({'loginStatus': 'INVALID_USERNAME_OR_PASSWORD'})


def test_keep_alive_endpoint(logged_in_client):
    assert logged_in_client.keep_alive.timeout == 3.05
    assert logged_in_client.keep_alive._error == KeepAliveError
    assert logged_in_client.keep_alive._endpoints_uk.get('KeepAlive') == 'https://identitysso.betfair.com/api/keepAlive'


def test_keep_alive_error_handler(logged_in_client):
    assert logged_in_client.keep_alive._error_handler({'status': 'SUCCESS'}) is None
    with pytest.raises(KeepAliveError):
        logged_in_client.keep_alive._error_handler({'status': 'FAIL', 'error': 'NO_SESSION'})


def test_logout_endpoint(logged_in_client):
    assert logged_in_client.logout.timeout == 3.05
    assert logged_in_client.logout._error == LogoutError
    assert logged_in_client.logout._endpoints_uk.get('Logout') == 'https://identitysso.betfair.com/api/logout'


def test_logout_error_handler(logged_in_client):
    assert logged_in_client.logout._error_handler({'status': 'SUCCESS'}) is None
    with pytest.raises(LogoutError):
        logged_in_client.logout._error_handler({'status': 'FAIL', 'error': 'NO_SESSION'})
