import pytest

from betfairlightweight import APIClient
from betfairlightweight.endpoints.base import BaseEndpoint


@pytest.fixture
def client():
    return APIClient('username', 'password', 'app_key', 'UK')


@pytest.fixture
def client_aus():
    return APIClient('username', 'password', 'app_key', 'AUS')


@pytest.fixture
def logged_in_client():
    client = APIClient('username', 'password', 'app_key', 'UK')
    client.set_session_token('sessiontoken')
    return client


@pytest.fixture
def logged_in_client_aus():
    client = APIClient('username', 'password', 'app_key', 'AUS')
    client.set_session_token('sessiontoken')
    return client


@pytest.fixture
def client_base_endpoint():
    client = APIClient('username', 'password', 'app_key', 'UK')
    client.set_session_token('sessiontoken')
    base_endpoint = BaseEndpoint(client)
    return base_endpoint
