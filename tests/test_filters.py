import unittest

from betfairlightweight.filters import MarketFilter, StreamingMarketDataFilter, StreamingMarketFilter


class MarketFilterTest(unittest.TestCase):

    def setUp(self):
        self.market_filter = MarketFilter()

    def test_init(self):
        assert self.market_filter.text_query is None
        assert self.market_filter.event_type_ids == []
        assert self.market_filter.event_ids == []
        assert self.market_filter.competition_ids == []
        assert self.market_filter.market_ids == []
        assert self.market_filter.venues == []
        assert self.market_filter.bsp_only is None
        assert self.market_filter.turn_in_play_enabled is None
        assert self.market_filter.in_play_only is None
        assert self.market_filter.market_betting_types == []
        assert self.market_filter.market_type_codes == []
        assert self.market_filter.market_countries == []
        assert self.market_filter.market_start_time is None
        assert self.market_filter.with_orders == []

    def test_serialise(self):
        assert self.market_filter.serialise == {
            'marketIds': [],
            'textQuery': None,
            'marketBettingTypes': [],
            'eventTypeIds': [],
            'eventIds': [],
            'turnInPlayEnabled': None,
            'inPlayOnly': None,
            'marketTypeCodes': [],
            'venues': [],
            'marketCountries': [],
            'bspOnly': None,
            'competitionIds': [],
            'marketStartTime': None,
            'withOrders': [],
        }


class StreamingMarketFilterTest(unittest.TestCase):

    def setUp(self):
        self.market_filter = StreamingMarketFilter()

    def test_init(self):
        assert self.market_filter.market_ids == []
        assert self.market_filter.bsp_market is None
        assert self.market_filter.betting_types == []
        assert self.market_filter.event_type_ids == []
        assert self.market_filter.event_ids == []
        assert self.market_filter.turn_in_play_enabled is None
        assert self.market_filter.market_types == []
        assert self.market_filter.venues == []
        assert self.market_filter.country_codes == []

    def test_serialise(self):
        assert self.market_filter.serialise == {
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

    def test_init(self):
        assert self.market_filter.fields == self.fields
        assert self.market_filter.ladder_levels == self.ladder_levels

    def test_serialise(self):
        assert self.market_filter.serialise == {
            'fields': self.fields,
            'ladderLevels': self.ladder_levels
        }
