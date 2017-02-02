import unittest

from betfairlightweight.filters import MarketFilter, StreamingMarketDataFilter, StreamingMarketFilter


class MarketFilterTest(unittest.TestCase):

    def setUp(self):
        self.market_filter = MarketFilter()

    def test_return(self):
        assert self.market_filter == {
            'marketIds': None,
            'textQuery': None,
            'marketBettingTypes': None,
            'eventTypeIds': None,
            'eventIds': None,
            'turnInPlayEnabled': None,
            'inPlayOnly': None,
            'marketTypeCodes': None,
            'venues': None,
            'marketCountries': None,
            'bspOnly': None,
            'competitionIds': None,
            'marketStartTime': None,
            'withOrders': None,
        }


class StreamingMarketFilterTest(unittest.TestCase):

    def setUp(self):
        self.market_filter = StreamingMarketFilter()

    def test_return(self):
        assert self.market_filter == {
            'marketIds': [],
            'bspMarket': None,
            'bettingTypes': [],
            'eventTypeIds': [],
            'eventIds': [],
            'turnInPlayEnabled': None,
            'marketTypes': [],
            'venues': [],
            'countryCodes': [],
        }


class StreamingMarketDataFilterTest(unittest.TestCase):

    def setUp(self):
        self.fields = [1, 2, 3]
        self.ladder_levels = 69
        self.market_filter = StreamingMarketDataFilter(self.fields, self.ladder_levels)

    def test_return(self):
        assert self.market_filter == {
            'fields': self.fields,
            'ladderLevels': self.ladder_levels
        }
