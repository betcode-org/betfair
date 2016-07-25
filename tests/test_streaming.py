import datetime
import pytest
import time
import queue

from .fixtures import client
from .fixtures import logged_in_client, logged_in_client_aus

from betfairlightweight import APIClient
from betfairlightweight import StreamListener
from betfairlightweight.exceptions import TransactionCountError, AppKeyError
from betfairlightweight.streaming.stream import Stream


# def test_betfair_stream(logged_in_client):
#     betfair_stream = logged_in_client.create_stream(2)
#     assert betfair_stream.session_token == 'sessiontoken'
#     assert betfair_stream.timeout == 6
#     assert betfair_stream.buffer_size == 1024
#
#     assert not betfair_stream._running
#     betfair_stream.start(True)
#     assert betfair_stream._running
#     betfair_stream.stop()
#     assert not betfair_stream._running


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


def test_stream_heartbeat():
    output_queue = queue.Queue()
    stream = Stream(2, 'test stream', output_queue)

    heartbeat = {'id': 2, 'ct': 'HEARTBEAT', 'pt': 1465631102405, 'clk': 'ADgAcABpAHQIQ==', 'op': 'ocm'}
    stream.on_heartbeat(heartbeat)
    assert stream.unique_id == 2
    assert stream.stream_type == 'test stream'
    assert stream.output_queue == output_queue
    assert stream._clk == 'ADgAcABpAHQIQ=='
    assert stream._updates_processed == 0


def test_stream_ocm():
    output_queue = queue.Queue()
    stream = Stream(2, 'test stream', output_queue)
    assert stream._caches == {}

    sub_image = {'initialClk': 'Go/Tl34fu9KhfxyprqN/GrrGunH8fvvasfQ==', 'clk': 'AAAAAAAAAAAAA==', 'op': 'ocm',
                 'heartbeatMs': 5000, 'pt': 1465631379410, 'conflateMs': 0, 'id': 2, 'ct': 'SUB_IMAGE'}
    stream.on_subscribe(sub_image, 'ocm')
    assert stream._clk == 'AAAAAAAAAAAAA=='
    assert stream._initial_clk == 'Go/Tl34fu9KhfxyprqN/GrrGunH8fvvasfQ=='
    assert stream._updates_processed == 0
    assert stream._caches == {}

    update = {'oc': [{'id': '1.125207238',
                      'orc': [{'id': 10075521, 'fullImage': True,
                               'uo': [{'side': 'L', 'rc': 'REG_GGC', 'pt': 'L', 's': 2, 'sm': 0, 'rac': '',
                                       'sr': 2, 'sl': 0, 'pd': 1465631675000, 'id': '69689205956', 'p': 1.01,
                                       'status': 'E', 'ot': 'L', 'sc': 0, 'sv': 0}]}]}],
              'id': 2, 'op': 'ocm','clk': 'ANsJAK4OAMQJAJwHAMQD', 'pt': 1465631675560}
    stream.on_update(update, 'ocm')
    assert stream._clk == 'ANsJAK4OAMQJAJwHAMQD'
    assert stream._updates_processed == 1
    assert len(stream._caches) == 1

    # stream.on_resubscribe()


def test_stream_mcm():
    output_queue = queue.Queue()
    stream = Stream(2, 'test stream', output_queue)
    assert stream._caches == {}

    sub_image = {'id': 2, 'ct': 'SUB_IMAGE', 'pt': 1465634309598, 'clk': 'AAAAAAAA', 'heartbeatMs': 5000,
                 'conflateMs': 0, 'mc': [{'marketDefinition': {'regulators': ['MR_INT'], 'discountAllowed': True,'bettingType': 'ODDS', 'runners': [{'id': 10075521,'sortPriority': 1, 'status': 'ACTIVE', 'adjustmentFactor': 46.183}, {'id': 10103089, 'sortPriority': 2, 'status': 'ACTIVE', 'adjustmentFactor': 15.625}, {'id': 9901125, 'sortPriority': 3, 'status': 'ACTIVE', 'adjustmentFactor': 8}, {'id': 10058017, 'sortPriority': 4, 'status': 'ACTIVE', 'adjustmentFactor': 7.692}, {'id': 9495964, 'sortPriority': 5, 'status': 'ACTIVE', 'adjustmentFactor': 6.667}, {'id': 7580872, 'sortPriority': 6, 'status': 'ACTIVE', 'adjustmentFactor': 4.762}, {'id': 9493948, 'sortPriority': 7, 'status': 'ACTIVE', 'adjustmentFactor': 4.167}, {'id': 346313, 'sortPriority': 8, 'status': 'ACTIVE', 'adjustmentFactor': 3.571}, {'id': 9500667, 'sortPriority': 9, 'status': 'ACTIVE', 'adjustmentFactor': 3.333}], 'numberOfWinners': 1, 'marketTime': '2016-06-11T12:40:00.000Z', 'bspReconciled': False, 'marketBaseRate': 5, 'eventTypeId': '7', 'eventId': '27824490', 'countryCode': 'GB', 'runnersVoidable': False, 'inPlay': False, 'numberOfActiveRunners': 9, 'complete': True, 'version': 1337603119, 'suspendTime': '2016-06-11T12:40:00.000Z', 'venue': 'Sandown', 'bspMarket': True, 'timezone': 'Europe/London', 'marketType': 'WIN', 'betDelay': 0, 'crossMatching': False, 'openDate': '2016-06-11T12:40:00.000Z', 'persistenceEnabled': True, 'turnInPlayEnabled': True, 'status': 'OPEN'}, 'id': '1.125207238', 'rc': [{'batl': [[0, 24, 21.64]], 'batb': [[0, 22, 12.11]], 'id': 10058017}, {'batl': [[0, 14, 11.56]], 'batb': [[0, 13, 19.86]], 'id': 9901125}, {'batl': [[0, 50, 6.33]], 'batb': [[0, 36, 2.13]], 'id': 9500667}, {'batl': [[0, 24, 20.28]], 'batb': [[0, 22, 10.47]], 'id': 7580872}, {'batl': [[0, 28, 3.35]], 'batb': [[0, 27, 2.79]], 'id': 346313}, {'batl': [[0, 5.2, 23.93]], 'batb': [[0, 5.1, 30]], 'id': 10103089}, {'batl': [[0, 2.08, 683.93]], 'batb': [[0, 2.06, 3.17]], 'id': 10075521}, {'batl': [[0, 28, 3.58]], 'batb': [[0, 21, 31.7]], 'id': 9495964}, {'batl': [[0, 15, 19.8]], 'batb': [[0, 13, 2.9]], 'id': 9493948}], 'img': True}],
                 'initialClk': '0weX5+3iCdMHupXD5QnTB6SQ9ugJ', 'op': 'mcm'}
    stream.on_subscribe(sub_image, 'mcm')
    assert stream._clk == 'AAAAAAAA'
    assert stream._initial_clk == '0weX5+3iCdMHupXD5QnTB6SQ9ugJ'
    assert len(stream._caches) == 1

    update = {'pt': 1465635079508,
              'mc': [{'rc': [{'id': 9495964, 'batb': [[0, 22, 4]]}], 'id': '1.125207238'}],
              'id': 2, 'clk': 'AJoBAJwBALEB', 'op': 'mcm'}
    stream.on_update(update, 'mcm')
    assert stream._clk == 'AJoBAJwBALEB'
    assert stream._updates_processed == 1
    assert len(stream._caches) == 1

    # stream.on_resubscribe()
