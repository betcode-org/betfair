import unittest
from unittest import mock

from betfairlightweight.resources.streamingresources import MarketDefinition
from tests.tools import create_mock_json


class TestMarketDefinition(unittest.TestCase):

    def setUp(self):
        self.mock_response = create_mock_json('tests/resources/streaming_market_definition.json')
        self.market_definition = MarketDefinition(**self.mock_response.json())

    def test_init(self):
        assert self.market_definition._data == self.mock_response.json()
        assert len(self.market_definition.runners) == 7
        assert self.market_definition.bsp_market is True
        assert self.market_definition.market_base_rate == 5
