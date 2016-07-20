import pytest

from betfairlightweight.apiclient import APIClient


@pytest.fixture
def client():
    return APIClient('username', 'password', 'app_key', 'UK')


@pytest.fixture
def logged_in_client(client):
    client = APIClient('username', 'password', 'app_key', 'UK')
    client.set_session_token('sessiontoken', 'testcall')
    return client


@pytest.fixture
def logged_in_client_aus(client):
    client = APIClient('username', 'password', 'app_key', 'AUS')
    client.set_session_token('sessiontoken', 'testcall')
    return client
