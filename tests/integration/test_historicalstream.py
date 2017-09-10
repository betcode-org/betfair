import unittest

import betfairlightweight
from betfairlightweight import StreamListener


class HistoricalStreamTest(unittest.TestCase):

    def test_historical_stream(self):
        trading = betfairlightweight.APIClient('username', 'password')
        stream = trading.streaming.create_historical_stream(
            directory='tests/resources/historicaldata/BASIC-1.132153978',
            listener=StreamListener()
        )
        stream.start(async=False)

        assert stream.listener.stream_type == 'marketSubscription'
        assert stream.listener.stream_unique_id == 'HISTORICAL'
        assert stream.listener.clk == '3522512789'

        assert stream.listener.stream._updates_processed == 479
        assert len(stream.listener.stream._caches) == 1

        market = stream.listener.stream._caches.get('1.132153978')
        assert len(market.runners) == 14
