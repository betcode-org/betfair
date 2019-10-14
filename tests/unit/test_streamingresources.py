import unittest

from betfairlightweight.resources.streamingresources import (
    MarketDefinition,
    MarketDefinitionRunner,
)
from tests.unit.tools import create_mock_json


class TestMarketDefinition(unittest.TestCase):
    def setUp(self):
        self.mock_response = create_mock_json(
            "tests/resources/streaming_market_definition.json"
        )
        self.market_definition = MarketDefinition(**self.mock_response.json())

    def test_init(self):
        assert len(self.market_definition.runners) == 7
        assert self.market_definition.bsp_market is True
        assert self.market_definition.market_base_rate == 5
        assert len(self.market_definition.key_line_definitions.key_line) == 2

    def test_missing_open_date(self):
        response_json = dict(self.mock_response.json())
        response_json.pop("openDate")
        market_definition = MarketDefinition(**response_json)
        assert market_definition.open_date is None


class TestMarketDefinitionRunner(unittest.TestCase):
    def setUp(self):
        self.mock_response = create_mock_json(
            "tests/resources/streaming_market_definition.json"
        )
        market_definition = self.mock_response.json()
        runner = market_definition["runners"][0]
        self.market_definition_runner = MarketDefinitionRunner(**runner)

    def test_init(self):
        assert self.market_definition_runner.selection_id == 11131804
        assert self.market_definition_runner.adjustment_factor == 44.323
        assert self.market_definition_runner.sort_priority == 1
        assert self.market_definition_runner.status == "ACTIVE"
        assert self.market_definition_runner.removal_date is None

    def test_str(self):
        assert str(self.market_definition_runner) == "MarketDefinitionRunner: 11131804"

    def test_repr(self):
        assert repr(self.market_definition_runner) == "<MarketDefinitionRunner>"
