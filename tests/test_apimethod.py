import pytest
import json

from fixtures import client
from fixtures import logged_in_client

from betfairlightweight import apimethod
from betfairlightweight.errors.apiexceptions import BetfairError, APIError, LoginError, LogoutError, KeepAliveError


def test_api_method_init(logged_in_client):
    request = apimethod.APIMethod(logged_in_client, 'method', 'params', 'exchange')
    assert request._api_client == logged_in_client
    assert request.method == 'method'
    assert request.params == 'params'
    assert request.exchange == 'exchange'
    assert request.instructions_length == 0
    assert request.create_req == json.dumps({'jsonrpc': '2.0',
                                             'method': request.method,
                                             'params': request.params,
                                             'id': 1})
    with pytest.raises(BetfairError):
        request()


def test_api_method_init_order(logged_in_client):
    request = apimethod.APIMethod(logged_in_client, 'SportsAPING/v1.0/placeOrders',
                                  {'instructions': [1, 2, 3]}, 'exchange')
    assert request.instructions_length == 3


def test_api_method_create_resp(logged_in_client):
    request_object = type('obj', (object,), {'status_code': 'error'})

    request = apimethod.APIMethod(logged_in_client, 'method', 'params', 'exchange')
    with pytest.raises(APIError):
        request.create_resp(request_object, None)
