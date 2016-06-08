import datetime
import pytest
import time

from fixtures import client
from fixtures import logged_in_client, logged_in_client_aus

from betfairlightweight import APIClient
from betfairlightweight import StreamListener
from betfairlightweight.errors.apiexceptions import TransactionCountError, AppKeyError


def test_betfair_stream(logged_in_client):
    betfair_stream = logged_in_client.create_stream(2)
    assert betfair_stream.session_token == 'sessiontoken'
    assert betfair_stream.timeout == 6
    assert betfair_stream.buffer_size == 1024

    assert not betfair_stream.running
    betfair_stream.start(True)
    assert betfair_stream.running
    betfair_stream.stop()
    assert not betfair_stream.running


def test_stream_listener():
    listener = StreamListener()

    # op: connection

    raw_data = '{"op":"connection","connectionId":"003-080616112551-10594"}\r\n'
    assert listener.on_data(raw_data) == None

    raw_data = """{"op":"status","id":2,"statusCode":"SUCCESS","connectionClosed":false}"""
    assert listener.on_data(raw_data) == None

    raw_data = '{"op":"status","id":2,"statusCode":"FAILURE","errorCode":"NO_APP_KEY","errorMessage":' \
               '"AppKey not set","connectionClosed":true,"connectionId":"001-080616112836-9540"}\r\n'
    assert listener.on_data(raw_data) == False

    raw_data = '{"op":"status","id":2,"statusCode":"FAILURE","errorCode":"SUBSCRIPTION_LIMIT_EXCEEDED ",' \
               '"errorMessage":"Limit reached","connectionClosed":false,"connectionId":"001-080616112836-9540"}\r\n'
    assert listener.on_data(raw_data) == None
