import json
import unittest
import pytest

from .fixtures import client
from .fixtures import logged_in_client, logged_in_client_aus

from betfairlightweight.apiclient import APIClient
from betfairlightweight.endpoints.base import BaseEndpoint
from betfairlightweight.exceptions import APIError, LoginError, LogoutError, KeepAliveError


def test_base_endpoint_init(logged_in_client):
    base_endpoint = BaseEndpoint(logged_in_client)
    assert base_endpoint.timeout == 3.05
    assert base_endpoint._error == APIError
    assert base_endpoint.exchange == logged_in_client.exchange


class BaseEndpointTest(unittest.TestCase):

    def setUp(self):
        client = APIClient('username', 'password', 'app_key', 'UK')
        client.set_session_token('sessiontoken')
        self.base_endpoint = BaseEndpoint(client)

    def test_create_resp(self):
        pass

    def test_create_req(self):
        payload = {'jsonrpc': '2.0',
                   'method': 'test',
                   'params': 'empty',
                   'id': 1}
        assert self.base_endpoint.create_req('test', 'empty') == json.dumps(payload)

    def test_error_handler(self):
        response = {'result': 'empty'}
        self.base_endpoint._error_handler(response)

        response = {'error': {'code': -32700}}
        with pytest.raises(APIError):
            self.base_endpoint._error_handler(response)


def test_login_endpoint(logged_in_client):
    assert logged_in_client.login.timeout == 3.05
    assert logged_in_client.login._error == LoginError
    assert logged_in_client.login._endpoints_uk.get('Login') == 'https://identitysso.betfair.com/api/certlogin'

    assert logged_in_client.login._error_handler({'loginStatus': 'SUCCESS'}) is None
    with pytest.raises(LoginError):
        logged_in_client.login._error_handler({'loginStatus': 'INVALID_USERNAME_OR_PASSWORD'})


def test_keep_alive_endpoint(logged_in_client):
    assert logged_in_client.keep_alive.timeout == 3.05
    assert logged_in_client.keep_alive._error == KeepAliveError
    assert logged_in_client.keep_alive._endpoints_uk.get('KeepAlive') == 'https://identitysso.betfair.com/api/keepAlive'

    assert logged_in_client.keep_alive._error_handler({'status': 'SUCCESS'}) is None
    with pytest.raises(KeepAliveError):
        logged_in_client.keep_alive._error_handler({'status': 'FAIL'})


def test_logout_endpoint(logged_in_client):
    assert logged_in_client.logout.timeout == 3.05
    assert logged_in_client.logout._error == LogoutError
    assert logged_in_client.logout._endpoints_uk.get('Logout') == 'https://identitysso.betfair.com/api/logout'

    assert logged_in_client.logout._error_handler({'status': 'SUCCESS'}) is None
    with pytest.raises(LogoutError):
        logged_in_client.logout._error_handler({'status': 'FAIL'})
