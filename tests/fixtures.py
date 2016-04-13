import pytest

from betfairlightweight.apiclient import APIClient


@pytest.fixture
def client():
    return APIClient('username', 'password', 'UK')


@pytest.fixture
def logged_in_client(client):
    client = APIClient('username', 'password', 'UK')
    client.set_session_token('sessiontoken', 'testcall')
    return client


@pytest.fixture
def logged_in_client_aus(client):
    client = APIClient('username', 'password', 'AUS')
    client.set_session_token('sessiontoken', 'testcall')
    return client
