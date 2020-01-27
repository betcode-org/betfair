import unittest

import betfairlightweight
from betfairlightweight import StreamListener


class HistoricalStreamTest(unittest.TestCase):
    def test_historical_stream(self):
        trading = betfairlightweight.APIClient("username", "password", app_key="appKey")
        stream = trading.streaming.create_historical_stream(
            directory="tests/resources/historicaldata/BASIC-1.132153978",
            listener=StreamListener(),
        )
        stream.start()

        assert stream.listener.stream_type == "marketSubscription"
        assert stream.listener.stream_unique_id == 0
        assert stream.listener.clk == "3522512789"

        assert stream.listener.stream._updates_processed == 480
        assert len(stream.listener.stream._caches) == 1

        market = stream.listener.stream._caches.get("1.132153978")
        assert len(market.runners) == 14
        assert stream._running is False
