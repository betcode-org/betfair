import unittest

import betfairlightweight
from betfairlightweight import StreamListener


class HistoricalStreamTest(unittest.TestCase):

    def test_historical_stream(self):
        trading = betfairlightweight.APIClient('username', 'password', app_key='appKey')
        stream = trading.streaming.create_historical_stream(
            directory='tests/resources/historicaldata/BASIC-1.132153978',
            listener=StreamListener()
        )
        stream.start(_async=False)

        assert stream.listener.stream_type == 'marketSubscription'
        assert stream.listener.stream_unique_id == 'HISTORICAL'
        assert stream.listener.clk == '3522512789'

        assert stream.listener.stream._updates_processed == 480
        assert len(stream.listener.stream._caches) == 1

        market = stream.listener.stream._caches.get('1.132153978')
        assert len(market.runners) == 14
        assert stream._running is False


class HistoricalRaceStreamTest(unittest.TestCase):

    def test_historical_stream(self):
        trading = betfairlightweight.APIClient('username', 'password', app_key='appKey')
        stream = trading.streaming.create_historical_stream(
            directory='tests/resources/historicaldata/RACE-1.140075353',
            listener=StreamListener(),
            operation='raceSubscription'
        )
        stream.start(_async=False)

        assert stream.listener.stream_type == 'raceSubscription'
        assert stream.listener.stream_unique_id == 'HISTORICAL'

        assert stream.listener.stream._updates_processed == 2
        assert len(stream.listener.stream._caches) == 1

        market = stream.listener.stream._caches.get('1.1234567')
        assert len(market.rrc) == 2
        assert stream._running is False
